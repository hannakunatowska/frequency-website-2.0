const images = [
    "static/data/images/spectrum1.png",
    "static/data/images/spectrum2.png",
    "static/data/images/spectrum3.png",
    "static/data/images/spectrum4.png",
    "static/data/images/spectrum5.png",
    "static/data/images/spectrum6.png",
    "static/data/images/spectrum7.png",
    "static/data/images/spectrum8.png"
];

let current = 0;

const spectrumImg = document.getElementById("spectrum");
const buttons = document.querySelectorAll(".side-menu button");

function changeImage(newIndex) {

    /*
    Changes image (with fade).

    Arguments:
        "newIndex"
    
    Returns:
        None
    */

    spectrumImg.style.opacity = 0;
    setTimeout(() => {
        spectrumImg.src = images[newIndex];
        spectrumImg.style.opacity = 1;
    }, 250);
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

function updateActiveButton() {
    buttons.forEach((btn, idx) => {
        btn.classList.toggle("active", idx === current);
    });
}

// Attach click event to all buttons
buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
        const index = parseInt(btn.getAttribute("data-index"));
        changeImage(index);
    });
});

// Initialize
updateActiveButton();
