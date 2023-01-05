const parallax = document.querySelector("main")

window.addEventListener("scroll",function(){
    let offset = window.pageYOffset;
    parallax.style.backgroundPositionY = offset * 0.1 + "px";
})