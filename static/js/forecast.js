const loadingScreen = document.getElementById("loading-screen");
const errorScreen = document.getElementById("error-screen");
const reportContent = document.getElementById("report-content");
const errorMessage = document.getElementById("error-message")

function showLoadingScreen(){
  loadingScreen.hidden = false;
  errorScreen.hidden = true;
  reportContent.hidden = true;
}

function showErrorScreen(message){
  loadingScreen.hidden = true;
  errorScreen.hidden = false;
  reportContent.hidden = true;
  errorMessage.textContent = message;
}

function showReport(){
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
        status = await retrieveForecastStatus();
        if(status.status === "error"){
          showErrorScreen(status.error);
          clearInterval(intervalId);
        }
        if(status.status === "ready"){
          showReport();
          clearInterval(intervalId);
        }
      }
      catch(error) {
        showErrorScreen(error.message);
        clearInterval(intervalId);
      }
    }, 5000
  )
}

async function loadLatestReport(){
  const response = await fetch("/api/forecast/latest");
  if(!response.ok){
    throw new Error("Latest report is not available at the moment.");
  }
  const result = response.json();
  if(result.status === "unavailable"){
    throw new Error("Latest report is not available at the moment.");
  }
  document.getelementById("report-metadata").innerHTML = '<p> ${result.report} </p>'
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
      showReport();
      return;
    }
    if(status.status === "error") {
      showErrorScreen(status.error);
      return;
    }
  }
  catch(error) {
    showErrorScreen(error.message);
  }
}
