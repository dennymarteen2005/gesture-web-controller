chrome.runtime.onMessage.addListener((message) => {
  const gesture = message.gesture;

  if (!gesture || gesture === "NONE") return;

  const video = document.querySelector("video");

  console.log("Gesture received:", gesture);

  if (gesture === "PLAY_PAUSE" && video) {
    video.paused ? video.play() : video.pause();
  }

  if (gesture === "SCROLL_DOWN") {
    window.scrollBy({ top: 500, behavior: "smooth" });
  }

  if (gesture === "SCROLL_UP") {
    window.scrollBy({ top: -500, behavior: "smooth" });
  }
});
