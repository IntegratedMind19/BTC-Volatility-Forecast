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
