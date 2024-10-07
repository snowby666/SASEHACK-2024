const body2 = document.querySelector("body"),
modeToggle = document.querySelector(".dark-light");

      let getMode = localStorage.getItem("mode");
          if(getMode && getMode === "dark-mode"){
            body2.classList.add("dark");
          }

// js code to toggle dark and light mode
      modeToggle.addEventListener("click" , () =>{
        modeToggle.classList.toggle("active");
        body2.classList.toggle("dark");

        // js code to keep user selected mode even page refresh or file reopen
        if(!body2.classList.contains("dark")){
            localStorage.setItem("mode" , "light-mode");
        }else{
            localStorage.setItem("mode" , "dark-mode");
        }
      });