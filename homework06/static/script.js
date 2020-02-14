"use strict"
// Cylce through header menu items
// Apply active style to the one that matches current page
const menuItem = document.querySelectorAll('a.item')

for (var i=0; i<menuItem.length; i++) {
    if (menuItem[i].getAttribute('href') === window.location.pathname) {
        console.log(window.location.pathname)
        menuItem[i].classList.toggle("active")
        menuItem[i].firstElementChild.classList.toggle("teal")
        menuItem[i].firstElementChild.classList.toggle("left")
        menuItem[i].firstElementChild.classList.toggle("pointing")
    }
}