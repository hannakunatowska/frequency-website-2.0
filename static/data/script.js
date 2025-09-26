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
const overlay = document.getElementById('highlight-overlay');
const previewImage = document.getElementById('preview-image');

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

function updateActiveButton() {
    buttons.forEach((btn, idx) => {
        btn.classList.toggle("active", idx === current);
    });
}

buttons.forEach((btn) => {

    const index = parseInt(btn.getAttribute("data-index"));

    btn.addEventListener("click", () => {
        current = index;
        changeImage(current);
        overlay.style.opacity = '0';
        previewImage.style.opacity = '0';
        updateActiveButton();
    });

    btn.addEventListener('mouseenter', () => {

        const index = parseInt(btn.getAttribute("data-index"));

        if (index <= current) return;

        overlay.style.opacity = '1';

        previewImage.src = images[index];
        previewImage.style.display = 'block';
        previewImage.style.opacity = '1';

        const rect = btn.getBoundingClientRect();
        const previewHeight = previewImage.offsetHeight || 120;
        previewImage.style.top = `${rect.top + rect.height/2 - previewHeight/2}px`;
        previewImage.style.left = `${rect.right + 30}px`;
    });

    btn.addEventListener('mouseleave', () => {
        overlay.style.opacity = '0';
        previewImage.style.opacity = '0';
    });
});

// Initialize
updateActiveButton();
