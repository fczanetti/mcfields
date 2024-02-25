// ---------------------Configurações navbar-----------------------

const toggleButton = document.getElementById('toggle-button')
const navbarLinks = document.getElementById('navbar-links')

toggleButton.onclick = function() {
    navbarLinks.classList.toggle('active')
};

// ----------------------------------------------------------------

var navBar = document.getElementById('navbar');
window.onscroll = function() {
    if (window.scrollY > 22) {
        navBar.classList.add('scrolled');
    } else {
        navBar.classList.remove('scrolled');
    }
}