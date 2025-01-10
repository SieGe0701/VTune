// recorder.js
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
            console.log('Recording started');
            audioChunks = []; // Clear any previous recording
            recordingStatus.textContent = "Recording...";
            recordBtn.disabled = true;
            stopBtn.disabled = false;
            audioPlayerContainer.style.display = "none";
        };
        
        mediaRecorder.onstop = () => {
            console.log('Recording stopped');
            recordingStatus.textContent = "Recording stopped.";
            recordBtn.disabled = false;
            stopBtn.disabled = true;
            
            // Convert recorded audio to a Blob
            recordedBlob = new Blob(audioChunks, { type: "audio/webm" });
            console.log('Blob created:', recordedBlob.size, 'bytes');
            const audioURL = URL.createObjectURL(recordedBlob);
            
            // Set the audio URL to the player and make it visible
            audioPlayer.src = audioURL;
            audioPlayerContainer.style.display = "block";
        };
        
        mediaRecorder.ondataavailable = (e) => {
            console.log('Data chunk available:', e.data.size, 'bytes');
            audioChunks.push(e.data);
        };
        
        mediaRecorder.start();
    } catch (err) {
        console.error('Media recorder error:', err);
        alert("Could not access your microphone. Please allow microphone permissions.");
    }
});

stopBtn.addEventListener("click", () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
    }
});

// Function to convert blob to base64
const blobToBase64 = (blob) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => {
            console.log('Base64 conversion complete');
            resolve(reader.result);
        };
        reader.onerror = (error) => {
            console.error('Base64 conversion error:', error);
            reject(error);
        };
        reader.readAsDataURL(blob);
    });
};

uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    console.log('Form submission started');
    
    try {
        const formData = new FormData();
        
        // Check if there's a file upload
        const fileInput = document.getElementById("audio");
        if (fileInput.files.length > 0) {
            console.log('File upload detected:', fileInput.files[0].name);
            formData.append("audio", fileInput.files[0]);
        }
        // Check if there's a recording
        else if (recordedBlob) {
            console.log('Recording detected, size:', recordedBlob.size);
            // Convert blob to base64
            const base64Data = await blobToBase64(recordedBlob);
            console.log('Base64 data length:', base64Data.length);
            formData.append("recorded_audio", base64Data);
        } else {
            alert("Please either upload an audio file or make a recording.");
            return;
        }

        // Log form data entries
        for (let pair of formData.entries()) {
            console.log('Form data entry:', pair[0], 'length:', pair[1].length || pair[1].size);
        }
        
        console.log('Sending request to /recognize');
        const response = await fetch("/recognize", {
            method: "POST",
            body: formData
        });
        
        console.log('Response status:', response.status);
        console.log('Response headers:', [...response.headers.entries()]);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Server error response:', errorText);
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const resultHtml = await response.text();
        console.log('Received HTML response length:', resultHtml.length);
        
        // Create a temporary div to parse the HTML
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = resultHtml;
        
        // Check if there's an error message in the response
        const errorElement = tempDiv.querySelector('.error-message');
        if (errorElement) {
            throw new Error(errorElement.textContent);
        }
        
        // Replace the current page content with the result
        document.documentElement.innerHTML = resultHtml;
        
    } catch (error) {
        console.error("Detailed error during song recognition:", error);
        console.error("Error stack:", error.stack);
    }
});

// Log when the script loads
console.log('Recorder script loaded successfully');