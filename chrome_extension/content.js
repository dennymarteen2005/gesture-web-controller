chrome.runtime.onMessage.addListener((message) => {
  const g = message.gesture;
  if (!g || g === "NONE") return;

  const video = document.querySelector("video");

  if (g === "PLAY_PAUSE" && video) {
    video.paused ? video.play() : video.pause();
  }

  if (g === "SCROLL_DOWN") {
    window.scrollBy({ top: 500, behavior: "smooth" });
  }

  if (g === "SCROLL_UP") {
    window.scrollBy({ top: -500, behavior: "smooth" });
  }

  if (g === "NEXT_VIDEO") {
    const next = document.querySelector('a[aria-label="Next"]');
    if (next) next.click();
  }

  if (g === "PREV_VIDEO") {
    const prev = document.querySelector('a[aria-label="Previous"]');
    if (prev) prev.click();
  }
});
