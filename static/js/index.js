let data;
let analysis;

async function loadChartData(){
  try {
    const response = await fetch("/api/chart-data");
    const data = await response.json();
    drawVolChart(data);
  }
  catch(error) {
    console.error(error);
  }
}

async function loadAnalysisOutput(){
  try {
    const response = await fetch("/api/forecast");
    const analysis = await response.json();
  }
  catch(error){
    console.error(error);
  }
}

function drawVolatilityChart(data) {
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

loadChartData();
loadAnalysisOutput();

document.getElementById("price-btn").addEventListener("click", () => drawPriceData(data));
document.getElementById("vol-btn").addEventListener("click", () => drawVolatilityChart(data));
