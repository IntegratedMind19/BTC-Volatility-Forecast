let data;
let analysis;

async function loadChartData(){
    const response = await fetch("/api/chart-data");
    if (!response.ok){
      throw new Error(`Failed to load chart data, ${response.status}`);
    }
    data = await response.json();
}

async function loadAnalysisOutput(){
    const response = await fetch("/api/forecast");
    if (!response.ok){
        console.log("AAAAAA");
      throw new Error(`Failed to load forecast data, ${response.status}`);
    }
    analysis = await response.json();
}

function drawVolatilityChart() {
    console.log("Volatility button clicked");
    
    if (!data || !analysis){
      throw new Error("Chart or analysis is unavailable.");
    }
  
    const trace = {
        x: data.dates,
        y: data.vol,
        type: "scatter",
        mode: "lines",
        name: "Volatility"
    };

    const prediction = {
        x: ["Tomorrow"],
        y: [analysis.analysis.prediction.predicted_volatility],
        type: "scatter",
        mode: "lines",
        name: "prediction"
    };

    Plotly.react(
        "chart",
        [trace],
        {
            title: "Bitcoin Volatility (1 M)"
        }
    );
}

function drawPriceData(){
    console.log("Price button clicked");
    if (!data){
      throw new Error("Chart data is not available");
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

document.getElementById("price-btn").addEventListener("click", drawPriceData);
document.getElementById("vol-btn").addEventListener("click", drawVolatilityChart);
console.log("JavaScript file loaded successfully");
console.log(analysis);
initialize();
