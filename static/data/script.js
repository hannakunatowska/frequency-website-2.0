const images = ["static/data/images/spectrum1.png", "static/data/images/spectrum2.png", "static/data/images/spectrum3.png"]; // Add more if needed
let current = 0;

const spectrumImg = document.getElementById("spectrum");
const zoomInBtn = document.getElementById("zoomIn");
const zoomOutBtn = document.getElementById("zoomOut");

function changeImage(newIndex) {
    spectrumImg.style.opacity = 0; // start fade out
    setTimeout(() => {
        spectrumImg.src = images[newIndex];
        spectrumImg.style.opacity = 1; // fade in
    }, 250); // half of transition duration
}

function zoomIn() {
    if (current < images.length - 1) {
        current++;
        changeImage(current);
        zoomOutBtn.style.display = "inline-block";
    }
    if (current === images.length - 1) {
        zoomInBtn.style.display = "none";
    }
}

function zoomOut() {
    if (current > 0) {
        current--;
        changeImage(current);
        zoomInBtn.style.display = "inline-block";
    }
    if (current === 0) {
        zoomOutBtn.style.display = "none";
    }
}

// Button click events
zoomInBtn.addEventListener("click", zoomIn);
zoomOutBtn.addEventListener("click", zoomOut);

// Keyboard support
document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowRight") {
        zoomIn();
    } else if (event.key === "ArrowLeft") {
        zoomOut();
    }
});
