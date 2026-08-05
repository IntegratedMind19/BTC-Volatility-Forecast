let data;
const themebutton = document.getElementById("theme-toggle");

function applyTheme(theme){
    document.documentElement.setAttribute("data-theme", theme);
    if (theme === "dark"){
        themebutton.textContent = "Light mode";
    } else {
        themebutton.textContent = "Dark mode";
    }
}

function toggleTheme(){
    const current_theme = document.documentElement.getAttribute("data-theme");
    const next_theme = (current_theme === "dark" ? "light" : "dark");
    applyTheme(next_theme);
    localStorage.setItem("theme", next_theme);
}

function loadSavedTheme(){
    const saved_theme = localStorage.getItem("theme");
    applyTheme("saved_theme");
}

async function loadChartData(){
    const response = await fetch("/api/chart-data");
    if (!response.ok){
      throw new Error(`Failed to load chart data, ${response.status}`);
    }
    data = await response.json();
}

function drawVolatilityChart() {
    console.log("Volatility button clicked");
    
    if (!data){
      throw new Error("Chart data is not available.");
    }
  
    const trace = {
        x: data.dates,
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

    Plotly.react(
        "chart",
        [trace, prediction],
        {
            title: {
                "text": "Bitcoin Volatility"
            },
            xaxis: {
                "title": {
                    "text": "Dates (last 30 days)",
                    standoff: 30
                },
                tickangle: -45
            },
            yaxis: {
                "title": {
                    "text": "Volatility",
                    standoff: 30
                }
            },
            margin: { b: 200 },
            autosize: true
        },
        
        {responsive: true}
    );
}

function drawPriceChart(){
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
            title: {
                "text": "Bitcoin Price"
            },
            xaxis: {
                "title": {
                    "text": "Dates (last 30 days)",
                    standoff: 30
                },
                tickangle: -45
            },
            yaxis: {
                "title": {
                    "text": "Price (in USD)",
                    standoff: 30
                }
            },
            margin: { b: 200 },
            autosize: true
        },
        
        { responsive: true }
    );
}

async function initialize(){
  try {
    await loadChartData();
    await loadSavedTheme();
    await drawVolatilityChart();
  }
  catch(error){
    console.error(error);
  }
}

document.getElementById("price-btn").addEventListener("click", drawPriceChart);
document.getElementById("vol-btn").addEventListener("click", drawVolatilityChart);
themebutton.addEventListener("click", toggleTheme);
console.log("JavaScript file loaded successfully");
initialize();
