function toggleFormBlocks() {
    const mode = document.getElementById("modeSelect").value;

    document.getElementById("videoBlock").style.display = mode === "video" ? "block" : "none";
    document.getElementById("audioBlock").style.display = mode === "audio" ? "block" : "none";
    document.getElementById("textBlock").style.display = mode === "text" ? "block" : "none";
}
