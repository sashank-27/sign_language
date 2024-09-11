var videoStream = document.getElementById("video-stream");
var startBtn = document.getElementById("start-btn");
var stopBtn = document.getElementById("stop-btn");

// Start the video stream
function startStream() {
  videoStream.src = "http://localhost:5000/video_feed";
}

// Stop the video stream
function stopStream() {
  videoStream.src = "";
}

// Event listeners for buttons
startBtn.addEventListener("click", startStream);
stopBtn.addEventListener("click", stopStream);

// Reload the stream in case of errors
videoStream.onerror = function () {
  videoStream.src = videoStream.src;
};
