function toggleFormBlocks() {
    const mode = document.getElementById("modeSelect").value;
    document.getElementById("hiddenMode").value = mode;  // Met à jour le champ caché avec la valeur du mode
    console.log("Valeur du mode sélectionné :", mode);  // Affiche la valeur du mode dans la console

    document.getElementById("videoBlock").style.display = mode === "video" ? "block" : "none";
    document.getElementById("audioBlock").style.display = mode === "audio" ? "block" : "none";
    document.getElementById("textBlock").style.display = mode === "text" ? "block" : "none";
}
