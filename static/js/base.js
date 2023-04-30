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


