async function loadChartData(){
  try {
    const response = await fetch("/api/chart-data");
    const data = await response.json();
    drawVolChart(data);
  }
  catch(error) {
    console.error(error)
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

    Plotly.newPlot(
        "chart",
        [trace],
        {
            title: "Bitcoin Volatility"
        }
    );
}

loadChartData()
