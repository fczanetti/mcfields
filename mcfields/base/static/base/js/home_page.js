// Configurações carousel -------------------------------------

// Select all slides
const slides = document.querySelectorAll('.slide')

// loop through slides and set each slides translateX property to index * 100%
slides.forEach((slide, indx) => {
  slide.style.transform = `translateX(${indx * 100}%)`;
});

// current slide counter
let curSlide = 0;

// maximum number of slides
let maxSlide = slides.length - 1;

// select next slide button
const nextSlide = document.querySelector(".btn-next");

// select prev slide button
const prevSlide = document.querySelector(".btn-prev");

// add event listener and next slide functionality
nextSlide.addEventListener("click", function () {
  // check if current slide is the last and reset current slide
  if (curSlide === maxSlide) {
    curSlide = 0;
  } else {
    curSlide++;
  }
  slides.forEach((slide, indx) => {
    slide.style.transform = `translateX(${100 * (indx - curSlide)}%)`;
  });
});

// add event listener and navigation functionality
prevSlide.addEventListener("click", function () {
  // check if current slide is the first and reset current slide to last
  if (curSlide === 0) {
    curSlide = maxSlide;
  } else {
    curSlide--;
  }
  //   move slide by 100%
  slides.forEach((slide, indx) => {
    slide.style.transform = `translateX(${100 * (indx - curSlide)}%)`;
  });
});


// Configuração altura da div our-services da home page ----------------

// Verifica a altura do maior slide do carousel e ajusta a
// altura da div slider, tornando a altura da div our-services dinâmica.
let biggestSlideHeight = 0
slides.forEach((slide) => {
        let height = slide.offsetHeight
  if (biggestSlideHeight == 0) {
        biggestSlideHeight = height;
   }
   else if (slide.style.height > biggestSlideHeight) {
        biggestSlideHeight = slide.style.height;
   }
});
slider = document.getElementById('slider').style.height = `${biggestSlideHeight}px`

