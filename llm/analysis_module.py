from arch import arch_model
import yfinance as yf
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from scipy import stats
from datetime import datetime, timezone

class ForecastInputs:
    def __init__(self):
        self.btc = yf.download("BTC-USD", start = "2018-01-01")
        if self.btc.empty:
            raise Exception("Failed to retrieve Bitcoin historical price data.")
        self.btc = self.btc[["Close"]].dropna()
        log_diff = np.log(self.btc["Close"]).diff().dropna()
        
        try:
            res = arch_model(log_diff * 10, vol="GARCH", mean="ARX", lags=1, p=1, q=1, dist="t").fit(disp="off")
        except Exception as exc:
            raise RuntimeError("Fail to fit the GARCH model") from exc
            
        if isinstance(self.btc.columns, pd.MultiIndex):
            self.btc.columns = self.btc.columns.get_level_values(0)

        if "Close" not in self.btc.columns:
            raise ValueError("Bitcoin data does not contain a Close column.")
            
        self.btc = self.btc.iloc[1:].copy()
        self.btc["log_return"] = log_diff.values
        self.btc["garch_volatility"] = res.conditional_volatility / 10

        self.btc["return_lag_1"] = self.btc["log_return"].shift(1)
        self.btc["return_lag_2"] = self.btc["log_return"].shift(2)

        self.btc["garch_vol_lag_1"] = self.btc["garch_volatility"].shift(1)
        self.btc["garch_vol_lag_2"] = self.btc["garch_volatility"].shift(2)

        self.btc["rolling_mean_7"] = self.btc["log_return"].rolling(7).mean()

        self.btc["rolling_std_3"] = self.btc["log_return"].rolling(3).std()

        self.btc["rolling_std_7"] = self.btc["log_return"].rolling(7).std()

        self.btc["rolling_std_14"] = self.btc["log_return"].rolling(14).std()

        self.btc["target_volatility"] = self.btc["garch_volatility"].shift(-1)

        self.features = [
            "return_lag_1",
            "return_lag_2",
            "garch_vol_lag_1",
            "garch_vol_lag_2",
            "rolling_mean_7",
            "rolling_std_3",
            "rolling_std_7",
            "rolling_std_14"
        ]
        self.all_time_volatility = self.btc["garch_volatility"].dropna()
        self.all_time_features_data = self.btc[self.features].dropna().copy()
        self.last_feature_data = self.all_time_features_data.iloc[-1:]
        self.btc = self.btc.dropna().copy()

    def retrieve_features(self):
        self.feature_values = dict()
        for feature in self.features:
            self.feature_values[feature] = float(self.last_feature_data[feature].values[0])
        return self.feature_values

class Prediction:
    def __init__(self, forecast_input):
        self.forecast_input = forecast_input
        self.X = forecast_input.btc[forecast_input.features]
        self.y = forecast_input.btc["target_volatility"]
        self.monthly_avg = (
            forecast_input.all_time_volatility
            .iloc[-30:]
            .mean()
        )
        self.model = None
        self.pipeline = None
        self.prediction = None
        self.daily_threshold = None
        self.monthly_threshold = None
        self.feature_importance = None

    def train(self):
        self.model = RandomForestRegressor(
            n_estimators = 100,
            max_depth = 5,
            random_state = 123
        )

        self.pipeline = Pipeline([
            ("scaler", StandardScaler())
        ])

        self.X_scaled = self.pipeline.fit_transform(self.X)
        self.model.fit(self.X_scaled, self.y)

    def predict(self):
        if self.model is None or self.pipeline is None:
            self.train()
        last_scaled = self.pipeline.transform(self.forecast_input.last_feature_data)
        self.prediction = dict()
        self.prediction = float(self.model.predict(last_scaled)[0])
        if self.prediction >= float(self.forecast_input.all_time_volatility.iloc[-1]):
            self.direction = "higher"
        else:
            self.direction = "lower"
        return self.prediction

    def calculate_thresholds(self, data): #Calculate 33rd and 67th percentile
        thresholds = [np.percentile(data, 33), np.percentile(data, 67)]
        return thresholds

    def risk_level_judgement(self):
        if self.prediction is None:
            self.predict()
        if self.daily_threshold is None:
            self.daily_threshold = self.calculate_thresholds(self.forecast_input.all_time_volatility)
        if self.prediction > self.daily_threshold[1]:
            self.risk_level = "high"
        elif self.prediction < self.daily_threshold[0]:
            self.risk_level = "low"
        else:
            self.risk_level = "medium"
        return self.risk_level

    def vol_regime_judgement(self):
        if self.prediction is None:
            self.predict()
        if self.monthly_threshold is None:
            self.monthly_threshold = self.calculate_thresholds(self.forecast_input.all_time_volatility.rolling(30).mean().dropna())
        if self.monthly_avg < self.monthly_threshold[0]:
            self.vol_regime_level = "low"
        elif self.monthly_avg > self.monthly_threshold[1]:
            self.vol_regime_level = "high"
        else:
            self.vol_regime_level = "medium"

        self.vol_regime_percentile = stats.percentileofscore(self.forecast_input.all_time_volatility.rolling(30).mean().dropna(), self.monthly_avg)
        return {'vol_regime_level': self.vol_regime_level, 'vol_regime_percentile': float(self.vol_regime_percentile)}
        
    def retrieve_feature_importance(self):
        if self.model is None:
            self.train()
        if self.prediction is None:
            self.predict()
        self.feature_importance = dict()
        for i, feature in enumerate(self.forecast_input.features):
            self.feature_importance[feature] = float(self.model.feature_importances_[i]) * 100
        return self.feature_importance

class HistAnalysis:
  def __init__(self, forecast_input):
    self.forecast_input = forecast_input
    self.monthly_volatility = forecast_input.all_time_volatility.iloc[-30:]
    self.monthly_avg = self.monthly_volatility.mean()
    self.monthly_max = max(self.monthly_volatility)
    self.monthly_min = min(self.monthly_volatility)

  def trend_analysis(self):
    days = np.array([i for i in range(len(self.monthly_volatility))])
    i = 0
    self.slopes = list()
    while i + 29 < len(self.forecast_input.all_time_volatility):
      self.slopes.append(abs(np.polyfit(days, np.array(self.forecast_input.all_time_volatility.iloc[i:i+30]), deg = 1)[0]))
      i += 1
    self.trend = dict()
    self.slope = np.polyfit(days, np.array(self.monthly_volatility), deg = 1)[0]
    if self.slope > 0:
      self.trend['trend'] = "increasing"
    else:
      self.trend['trend'] = "decreasing"

    self.monthly_percentile = stats.percentileofscore(self.slopes[:-1], self.slopes[-1])
    if self.monthly_percentile > 67:
      self.trend['trend_strength'] = "strong"
    elif self.monthly_percentile < 33:
      if self.monthly_percentile < 17:
        self.trend['trend'] = "stable"
      else:
        self.trend['trend_strength'] = "weak"
    else:
      self.trend['trend_strength'] = "medium"
    return self.trend

  def persistence_analysis(self):
    self.persistence_index = float(self.monthly_volatility.autocorr(lag = 1))
    self.persistence = {'persistence_index': self.persistence_index}
    if self.persistence_index > 0.67:
      self.persistence['persistence_level'] = "strong"
    elif self.persistence_index < 0.33:
      self.persistence['persistence_level'] = "weak"
    else:
      self.persistence['persistence_level'] = "medium"
    return self.persistence

class Confidence:
  def __init__(self, forecast_input, pred, hist_analysis):
    self.forecast_input = forecast_input
    self.pred = pred
    self.hist_analysis = hist_analysis
    self.confidence_index = None
    self.confidence_level = None

  def confidence_analysis(self):
    if self.pred.prediction is None:
      self.pred.predict()

    self.persistence = self.hist_analysis.persistence_analysis()['persistence_index'] * 100

    self.tree_disagreements = list()
    for i in range(len(self.forecast_input.all_time_features_data)):
      sample = self.forecast_input.all_time_features_data.iloc[i:i+1]
      sample = self.pred.pipeline.transform(sample)
      self.prediction = float(self.pred.model.predict(sample)[0])
      self.individual_preds = np.array([float(tree.predict(sample)[0]) for tree in self.pred.model.estimators_])
      self.tree_disagreements.append(np.std(self.individual_preds) / max(abs(self.prediction), 1e-8))
    self.tree_disagreements_percentile = stats.percentileofscore(self.tree_disagreements[:-1], self.tree_disagreements[-1])

    self.confidence_index = 0.7 * (100 - self.tree_disagreements_percentile) + 0.3 * self.persistence

    if self.confidence_index > 67:
      self.confidence_level = "high"
    elif self.confidence_index < 33:
      self.confidence_level = "low"
    else:
      self.confidence_level = "medium"

    return {'confidence_level': self.confidence_level, 'confidence_index': self.confidence_index}

def get_analysis_data():
    forecast_input = ForecastInputs()
    pred = Prediction(forecast_input)
    hist_analysis = HistAnalysis(forecast_input)
    confidence = Confidence(forecast_input, pred, hist_analysis)
    try:
        analysis_output = {"prediction": {"predicted_volatility": pred.predict(),
                                          "forecast_relativity": pred.direction,
                                          "risk_level": pred.risk_level_judgement(),
                                          "volatility_regime": pred.vol_regime_judgement()},
                           "forecast_inputs": {"today_garch_volatility": float(forecast_input.all_time_volatility.iloc[-1]),
                                               "rolling_volatility": float(forecast_input.all_time_features_data['rolling_std_14'].iloc[-1]),
                                               "yesterday_volatility": float(forecast_input.all_time_volatility.iloc[-2]),
                                               "feature_values": forecast_input.retrieve_features(),
                                               "feature_importance": pred.retrieve_feature_importance()},
                           "historical_analysis": {"monthly_average": float(hist_analysis.monthly_avg),
                                                   "monthly_max": hist_analysis.monthly_max,
                                                   "monthly_min": hist_analysis.monthly_min,
                                                   "trend": hist_analysis.trend_analysis(),
                                                   "persistence": hist_analysis.persistence_analysis()},
                           "confidence": {"confidence_level": confidence.confidence_analysis()['confidence_level'],
                                          "confidence_index": float(confidence.confidence_index),
                                          "volatility_regime_percentile": float(pred.vol_regime_percentile),
                                          "persistence_index": confidence.persistence,
                                          "ensemble_uncertainty_percentile": float(confidence.tree_disagreements_percentile)},
                           "date_vol_and_price": {'vol': forecast_input.all_time_volatility.iloc[-29:].tolist(),
                                                  'price': forecast_input.btc["Close"].iloc[-29:].tolist(),
                                                 'date_price': forecast_input.btc["Close"].iloc[-29:].index.strftime('%d/%m/%Y').tolist(),
                                                 'date_vol': forecast_input.all_time_volatility.iloc[-29:].index.strftime('%d/%m/%Y').tolist()},
                           "metadata": {"timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                                        "model_version": "1.0"}
                           }
        return analysis_output
    except Exception as exc:
        return None
