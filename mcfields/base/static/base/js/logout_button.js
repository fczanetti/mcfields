// Customiza o botão que mostra o usuário logado e também permite o logout

logoutButton = document.getElementById('logout-button')
logoutButton.addEventListener('mouseover', change)
logoutButton.addEventListener('mouseleave', unchange)
originalText = logoutButton.innerText
function change() {
    logoutButton.style.backgroundColor = 'red';
    logoutButton.innerText = 'Sair';
}

function unchange() {
    logoutButton.style.backgroundColor = '#21642c';
    logoutButton.innerText = originalText;
}
