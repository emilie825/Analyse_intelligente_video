function toggleFormBlocks() {
    const mode = document.getElementById("modeSelect").value;
    document.getElementById("hiddenMode").value = mode;  // Met à jour le champ caché avec la valeur du mode
    console.log("Valeur du mode sélectionné :", mode);  // Affiche la valeur du mode dans la console

    document.getElementById("videoBlock").style.display = mode === "video" ? "block" : "none";
    document.getElementById("audioBlock").style.display = mode === "audio" ? "block" : "none";
    document.getElementById("textBlock").style.display = mode === "text" ? "block" : "none";
}

let slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("slide");
    let dots = document.getElementsByClassName("dot");

    if (n > slides.length) { slideIndex = 1; }
    if (n < 1) { slideIndex = slides.length; }

    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }

    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }

    slides[slideIndex-1].style.display = "block";
    dots[slideIndex-1].className += " active";
}

// Auto-advance slides every 5 seconds
setInterval(() => {
    plusSlides(1);
}, 5000);


document.querySelector('form').addEventListener('submit', function () {
    // Lancer le chargement après 1 seconde
    setTimeout(function () {
        // Afficher la barre de chargement
        const loadingBarContainer = document.getElementById("loadingBarContainer");
        const loadingBar = document.getElementById("loadingBar");
        loadingBarContainer.style.display = "block";

        // Afficher le spinner + texte
        document.getElementById("loadingOverlay").style.display = "block";

        // Animation de progression infinie
        let width = 0;
        const interval = setInterval(() => {
            width = (width + 1) % 100;
            loadingBar.style.width = width + "%";
        }, 30);
    }, 1000);
});

document.querySelector('form').addEventListener('submit', function () {
    const selectedLang = document.getElementById("langSelect").value;
    console.log("Langue sélectionnée :", selectedLang);
});

