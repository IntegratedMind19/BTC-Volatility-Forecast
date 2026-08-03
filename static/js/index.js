let data;
let analysis;

async function loadChartData(){
  try {
    const response = await fetch("/api/chart-data");
    if (!response.ok){
      throw new Error(`Failed to load chart data, ${response.status}`);
    }
    data = await response.json();
    drawVolatilityChart(data);
  }
}

async function loadAnalysisOutput(){
  try {
    const response = await fetch("/api/forecast");
    if (!response.ok){
      throw new Error(`Failed to load forecast data, ${response.status}`);
    }
    analysis = await response.json();
  }
}

function drawVolatilityChart(data) {
    if (!data || !analysis){
      console.error("Chart or analysis is unavailable.");
    }
  
    const trace = {
        x: data.dates,
        y: data.volatility,
        type: "scatter",
        mode: "lines",
        name: "Volatility"
    };

    const prediction = {
        x: ["Tomorrow"],
        y: [analysis.prediction.predicted_volatility],
        type: "scatter",
        mode: "lines",
        name: "prediction"
    };

    Plotly.react(
        "chart",
        [trace, prediction],
        {
            title: "Bitcoin Volatility (1 M)"
        }
    );
}

function drawPriceData(data){
    if (!data){
      console.error("Chart data is not available");
    }
    const trace = {
        x: data.dates,
        y: data.price,
        type: "scatter",
        mode: "lines",
        name: "Price"
    };

    Plotly.react(
      "chart",
      [trace],
      {
        title: "Bitcoin Price (1 M)"
      }
    );
}

async function initialize(){
  try {
    await Promise.all([loadChartData(), loadAnalysisOutput()]);
    drawVolatilityChart(data);
  }
  catch(error){
    console.error(error);
  }
}

document.getElementById("price-btn").addEventListener("click", () => drawPriceData(data));
document.getElementById("vol-btn").addEventListener("click", () => drawVolatilityChart(data));
console.log("JavaScript file loaded successfully");
initialize();
