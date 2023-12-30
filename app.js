var isSoundPlaying = false;
function detectDarkPattern() {
    // Simplified dark pattern detection logic
    var button = document.getElementById('checkButton');

    // For demonstration purposes, let's assume a dark pattern is detected
    if (button.classList.contains('dark-pattern-detected')) {
        playSoundAlert();
    }
}


function playSoundAlert() {
    var soundAlert = document.getElementById('darkPatternAlert');
    var modal = document.getElementById('myModal');
    var body = document.body;

    
    // Check if the sound element is defined and not null
    if (soundAlert) {
        soundAlert.play();
        soundAlert.loop = true; // Enable loop
        isSoundPlaying = true;

        // Make the body glow (add 'dark-pattern-detected' class)
        body.classList.add('dark-pattern-detected');

        // Display the modal
        modal.style.display = 'block';

        // Focus on the modal to trap keyboard focus
        modal.focus();
    }
}

function stopSound() {
    var soundAlert = document.getElementById('darkPatternAlert');
    var modal = document.getElementById('myModal');
    var body = document.body;

    // Check if the sound element is defined and not null
    if (soundAlert) {
        soundAlert.pause();
        soundAlert.currentTime = 0; // Reset the sound to the beginning
        isSoundPlaying = false;

        // Hide the modal
        modal.style.display = 'none';

        // Remove the 'dark-pattern-detected' class from the body
        body.classList.remove('dark-pattern-detected');
    }
}
