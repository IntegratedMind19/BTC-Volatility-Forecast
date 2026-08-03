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

    Plotly.newPlot(
      "chart",
      [trace],
      {
        title: "Bitcoin Price (1 M)"
      }
    );
}

loadChartData()
