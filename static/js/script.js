document.addEventListener("DOMContentLoaded", function () {
    let triggerSystem = document.querySelector(".input-field[name='trigger_system']");
    let triggerDuration = document.querySelector(".input-field[name='trigger_duration']");

    function toggleTriggerDuration() {
        if (triggerSystem.value === "Interrupteur manuel") {
            triggerDuration.disabled = true;
        } else {
            triggerDuration.disabled = false;
        }
    }

    // Vérifier au chargement de la page
    toggleTriggerDuration();

    // Ajouter un écouteur d'événement sur le changement
    triggerSystem.addEventListener("change", toggleTriggerDuration);
});