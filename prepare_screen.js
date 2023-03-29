setTimeout(() => {
    map_canvas = document.getElementsByClassName('game-layout__panorama')[0];
    map_canvas.requestFullscreen();
    setTimeout(() => {chrome.runtime.sendMessage("screen");}, 90);
}, 500);

