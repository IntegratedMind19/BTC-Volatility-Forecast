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
    document.dispatchEvent(
      new CustomEvent(
        "themechange",
        {detail: 
        {
          theme: next_theme
        }
        }
      )
    );
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

themebutton.addEventListener("click", toggleTheme);
loadSavedTheme();
