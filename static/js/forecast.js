const loadingScreen = document.getElementById("loading-screen");
const errorScreen = document.getElementById("error-screen");
const reportContent = document.getElementById("report-content");
const errorMessage = document.getElementById("error-message")

function showLoadingScreen(){
  console.log("Loading...");
  loadingScreen.hidden = false;
  errorScreen.hidden = true;
  reportContent.hidden = true;
}

function showErrorScreen(message){
  console.log("An error occured");
  loadingScreen.hidden = true;
  errorScreen.hidden = false;
  reportContent.hidden = true;
  errorMessage.textContent = message;
}

function showReport(){
  console.log("Report shown");
  loadingScreen.hidden = true;
  errorScreen.hidden = true;
  reportContent.hidden = false;
}

async function retrieveForecastStatus(){
  const response = await fetch("/api/forecast/status");
  if(!response.ok){
    throw new Error("Unable to get forecast status");
  }
  return response.json();
}

function pollUntilReady(){
  const intervalId = setInterval(
    async () => {
      try {
        const status = await retrieveForecastStatus();
        if(status.status === "error"){
          if(!status.previous_report_available){
            showErrorScreen(status.error);
          } else {
            console.log(status.error);
            await loadLatestReport();
          }
          return;
        }
        if(status.status === "ready"){
          await loadLatestReport();
          clearInterval(intervalId);
        }
      }
      catch(error) {
        showErrorScreen(error.message);
        clearInterval(intervalId);
      }
    }, 5000
  );
}

async function loadLatestReport(){
  const response = await fetch("/api/forecast/latest");
  if(!response.ok){
    throw new Error("Latest report is not available at the moment.");
  }
  const result = await response.json();
  if(result.status === "unavailable"){
    throw new Error("Latest report is not available at the moment.");
  }
  document.getElementById("report-metadata").innerHTML = marked.parse(result.report.metadata);
  document.getElementById("forecast-summary").innerHTML = marked.parse(result.report.forecast_summary);
  document.getElementById("feature-interpretation").innerHTML = marked.parse(result.report.feature_interpretation);
  document.getElementById("historical-trend").innerHTML = marked.parse(result.report.historical_trend_overview);
  document.getElementById("market-context").innerHTML = marked.parse(result.report.market_context);
  document.getElementById("model-confidence").innerHTML = marked.parse(result.report.confidence);
  document.getElementById("overall-summary").innerHTML = marked.parse(result.report.overall_summary);
  document.getElementById("model-limitations").innerHTML = marked.parse(result.report.model_limitations);
  showReport();
}

async function initializeForecastPage(){
  try {
    const status = await retrieveForecastStatus();
    if(status.status === "updating") {
      showLoadingScreen();
      pollUntilReady();
      return;
    }
    if(status.status === "ready") {
      await loadLatestReport();
      return;
    }
    if(status.status === "error") {
      if(!status.previous_report_available){
        showErrorScreen(status.error);
      } else {
        await loadLatestReport();
      }
      return;
    }
    showErrorScreen("Forecast status is unknown.");
  }
  catch(error) {
    showErrorScreen(error.message);
  }
}

initializeForecastPage();
