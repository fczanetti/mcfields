title = document.getElementById('id_title')
slugField = document.getElementById('id_slug');
title.addEventListener('change', debounce(updateSlug))

function slugify(text) {
return text
  .normalize('NFD')
  .replace(/[\u0300-\u036f]/g, '')
  .toLowerCase()
  .replace(/[^\w\s]/g, '')
  .replace(/\s+/g, '-')
  .trim();
}

function updateSlug(event) {
    slugField.value = slugify(event.target.value)
}

function debounce(func, timeout = 1000){
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => { func.apply(this, args); }, timeout);
  };
}
