chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        
        if (request === "screen") {

            var url = 'http://127.0.0.1:8000/send_gps_values/screen_capture/';
            fetch(url);
            return true;

        }

        if (request === "reset") {

            var url = 'http://127.0.0.1:8000/send_gps_values/reset_pictures/';
            fetch(url);
            return true;

        }

        if (request === "coords") {

            var url = 'http://127.0.0.1:8000/send_gps_values/process/';

            fetch(url)
            .then(response => response.json())
            .then(response => sendResponse({farewell: response}))
            .catch(error => console.log(error))
            return true;
        }

        if (request === "fullscreen") {

            chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                chrome.scripting.executeScript({
                    target : {tabId : tabs[0].id}, 
                    files : ['prepare_screen.js'],
                })
            });

        }

        if (request === "reload") {

            var url = 'http://127.0.0.1:8000/send_gps_values/reload/';
            fetch(url);
            return true;

        }

    }
);

