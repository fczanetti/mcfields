// ---------------------Configurações navbar-----------------------

const toggleButton = document.getElementById('toggle-button')
const navbarLinks = document.getElementById('navbar-links')
logoutButton = document.getElementById('logout-button')

toggleButton.onclick = function() {
    navbarLinks.classList.toggle('active')
    logoutButton.classList.toggle('inactive-button')
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