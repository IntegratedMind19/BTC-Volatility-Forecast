let data;
current_chart = "volatility";

function getChartTheme(){
    current_theme = document.documentElement.getAttribute("data-theme");
    if (current_theme === "dark"){
        return {
            background: "#121212",
            text: "#f1f1f1",
            grid: "#3a3a3a"
        };
    }
    else {
        return {
            background: "#ffffff",
            text: "#222222",
            grid: "#e5e5e5"
        };
    }
}

async function loadChartData(){
    const response = await fetch("/api/chart-data");
    if (!response.ok){
      throw new Error(`Failed to load chart data, ${response.status}`);
    }
    data = await response.json();
}

function drawVolatilityChart() {
    current_chart = "volatility";
    console.log("Volatility button clicked");
    
    if (!data){
      throw new Error("Chart data is not available.");
    }
  
    const trace = {
        x: data.date_vol,
        y: data.vol,
        type: "scatter",
        mode: "lines",
        name: "Volatility"
    };

    const prediction = {
        x: [data.tomorrow_date],
        y: [data.prediction],
        type: "scatter",
        mode: "markers",
        name: "prediction"
    };
    chart_theme = getChartTheme();
    Plotly.react(
        "chart",
        [trace, prediction],
        {
            title: {
                "text": "Bitcoin Volatility",
                color: chart_theme.text
            },
            font: {color: chart_theme.text},
            paper_bgcolor: chart_theme.background,
            plot_bgcolor: chart_theme.background,
            xaxis: {
                "title": {
                    "text": "Dates (last 30 days)",
                    standoff: 30,
                    color: chart_theme.text
                },
                tickangle: -45,
                gridcolor: chart_theme.grid
            },
            yaxis: {
                "title": {
                    "text": "Volatility",
                    standoff: 30,
                    color: chart_theme.text
                },
                gridcolor: chart_theme.grid
            },
            margin: { b: 200 },
            autosize: true
        },
        
        {responsive: true}
    );
}

function drawPriceChart(){
    current_chart = "price";
    console.log("Price button clicked");
    if (!data){
      throw new Error("Chart data is not available");
    }
    const trace = {
        x: data.dates.slice(0, 29),
        y: data.date_price,
        type: "scatter",
        mode: "lines",
        name: "Price"
    };
    const chart_theme = getChartTheme();
    Plotly.react(
      "chart",
      [trace],
        {
            title: {
                "text": "Bitcoin Close Price",
                color: chart_theme.text
            },
            font: { color: chart_theme.text },
            paper_bgcolor: chart_theme.background,
            plot_bgcolor: chart_theme.background,
            xaxis: {
                "title": {
                    "text": "Dates (last 30 days)",
                    standoff: 30,
                    color: chart_theme.text
                },
                tickangle: -45,
                gridcolor: chart_theme.grid
            },
            yaxis: {
                "title": {
                    "text": "Price (in USD)",
                    standoff: 30,
                    color: chart_theme.text
                },
                gridcolor: chart_theme.grid
            },
            margin: { b: 200 },
            autosize: true
        },
        
        { responsive: true }
    );
}

function updateCurrentChart(){
    if(!data){
        return;
    }
    if(current_chart === "volatility"){
        drawVolatilityChart();
    }
    else {
        drawPriceChart();
    }
}

async function initialize(){
  try {
    await loadChartData();
    await drawVolatilityChart();
  }
  catch(error){
    console.error(error);
  }
}

document.getElementById("price-btn").addEventListener("click", drawPriceChart);
document.getElementById("vol-btn").addEventListener("click", drawVolatilityChart);
document.addEventListener("themechange", updateCurrentChart);
console.log("JavaScript file loaded successfully");
initialize();
