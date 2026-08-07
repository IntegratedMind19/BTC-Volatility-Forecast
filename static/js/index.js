let data;
current_chart = "volatility";
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
    if (current_chart === "volatility"){
        drawVolatilityChart();
    }
    else {
        drawPriceChart();
    }
}

function loadSavedTheme(){
    const saved_theme = localStorage.getItem("theme");
    if (saved_theme === "dark" || saved_theme === "light") {
        applyTheme(saved_theme);
    }
    else {
        applyTheme("light");
    }
}

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
        y: data.price,
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
                "text": "Bitcoin Price",
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
