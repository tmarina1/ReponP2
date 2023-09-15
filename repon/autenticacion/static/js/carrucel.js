// JavaScript para el carrusel de fotos
const carousel = document.querySelector('.carousel');
const images = document.querySelectorAll('.carousel img');

let currentIndex = 0;

function nextImage() {
    currentIndex = (currentIndex + 1) % images.length;
    updateCarousel();
}

function prevImage() {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    updateCarousel();
}

function updateCarousel() {
    const translateX = -currentIndex * 100;
    carousel.style.transform = `translateX(${translateX}%)`;
}

setInterval(nextImage, 3000); // Cambiar la imagen cada 3 segundos (puedes ajustar el tiempo)

// Iniciar el carrusel
updateCarousel();