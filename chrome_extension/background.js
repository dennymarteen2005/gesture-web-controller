setInterval(async () => {
  try {
    const res = await fetch("http://localhost:5000/gesture");
    const data = await res.json();

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs.length === 0) return;
      chrome.tabs.sendMessage(tabs[0].id, {
        gesture: data.gesture
      });
    });
  } catch (e) {
    // server not running
  }
}, 300);
