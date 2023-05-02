// ONLOAD //

var header   = document.querySelector("header");
var mainImg  = document.querySelector("main .main-img");
var homedata = document.querySelector("section.home-data");
var footer   = document.querySelector("footer");

var result   = document.querySelector(".result");
window.onload = ()=>{
    setTimeout(()=>{
        header.style.visibility   = "visible";
        if(mainImg){
            mainImg.style.visibility  = "visible";
        }
        if(homedata){
            homedata.style.display    = "block";
        }
        if(result){
            result.style.display    = "block";
        }
        footer.style.display      = "table";
    },1000)
}

// CLICK NAVE //

var barmenu    = document.querySelector(".bar-menu");
var iconmenu   = document.querySelector(".icon-menu");
var iconcancel = document.querySelector(".icon-menu-cancel");
var nav        = document.querySelector("nav"); 
var navli      = nav.querySelectorAll("li");

const navClick = ()=>{
    for(let i = 0; i < navli.length; i++){
        navli[i].classList.toggle("click");
        navli[i].style.transitionDelay = "0." + i + "s";
    }
}

barmenu.onclick = ()=>{
    iconmenu.classList.toggle("click");
    iconcancel.classList.toggle("click");
    navClick()    
    nav.classList.toggle("click");    
}


