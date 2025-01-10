let mediaRecorder;
let audioChunks = [];
let recordingStatus = document.getElementById("recording-status");
let recordBtn = document.getElementById("record-btn");
let stopBtn = document.getElementById("stop-btn");
let audioPlayerContainer = document.getElementById("audio-player-container");
let audioPlayer = document.getElementById("audio-player");
let uploadForm = document.getElementById("upload-form");

let recordedBlob = null;

recordBtn.addEventListener("click", async () => {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert("Your browser does not support audio recording.");
        return;
    }

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.onstart = () => {
            recordingStatus.textContent = "Recording...";
            recordBtn.disabled = true;
            stopBtn.disabled = false;
        };

        mediaRecorder.onstop = () => {
            recordingStatus.textContent = "Recording stopped.";
            recordBtn.disabled = false;
            stopBtn.disabled = true;

            // Convert recorded audio to a Blob
            recordedBlob = new Blob(audioChunks, { type: "audio/webm" });
            const audioURL = URL.createObjectURL(recordedBlob);

            // Set the audio URL to the player and make it visible
            audioPlayer.src = audioURL;
            audioPlayerContainer.style.display = "block";
        };

        mediaRecorder.ondataavailable = (e) => {
            audioChunks.push(e.data);
        };

        mediaRecorder.start();
    } catch (err) {
        alert("Could not access your microphone. Please allow microphone permissions.");
        console.error(err);
    }
});

stopBtn.addEventListener("click", () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        audioChunks = [];
    }
});


