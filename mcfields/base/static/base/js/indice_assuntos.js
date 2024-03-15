const covers = document.querySelectorAll('.cover');

let hideList = (e) => {
    e.target.parentElement.nextElementSibling.classList.toggle('hidden-videos')
    e.target.nextElementSibling.nextElementSibling.classList.toggle('lightgray')
    e.target.nextElementSibling.nextElementSibling.classList.toggle('light-green')
};

covers.forEach((cover) => {
    cover.addEventListener('click', hideList)
})
