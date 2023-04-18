if (localStorage.getItem('coords') === null) {
    map_coords = [48.7101051, 2.1673017];
    var map = L.map('map').setView(map_coords, 16);

} else {
    map_coords = JSON.parse(localStorage.getItem('coords')).coords;
    var map = L.map('map').setView(map_coords, 1);
    L.marker(map_coords).addTo(map).bindPopup("<b>Prediction</b><br>Previous located point").openPopup();

    document.getElementById('display').disabled = false;
    document.getElementById('submit').disabled = false;
    //document.getElementById('autopin').disabled = false;
}


L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


async function get_screen() {

    window.close();
    
    chrome.runtime.sendMessage("fullscreen");
    document.getElementById('launch').disabled = true;
}

async function reset() {

    chrome.runtime.sendMessage("reset");
    document.getElementById('launch').disabled = true;

}

async function compute_coords() {
    
    document.getElementById('validation').innerHTML = 'The model is currently computing his predictions for this Geoguessr point. A message will appear when the work will be over.';

    chrome.runtime.sendMessage(
        "coords",
        function(response) {
            result = response.farewell;
            chrome.storage.sync.set({coords: [result.latitude, result.longitude], intermediate : [result.intermediate]})
            .then(() => {chrome.storage.sync.get('coords').then((coords) => {localStorage.setItem('coords', JSON.stringify(coords))})})
            .then(() => {chrome.storage.sync.get('intermediate').then((coords) => {localStorage.setItem('intermediate', JSON.stringify(coords))})})
            .then(() => {console.log("Value is set to " + [result.latitude, result.longitude]);})
            .then(() => {alert("Thanks for waiting ! The model has succesfully calculated his prediction for this point. You may close this window.");})
            .then(() => {document.getElementById('display').disabled = false})
            .then(() => {document.getElementById('submit').disabled = false})
            .then(() => {document.getElementById('load').disabled = false})
            .then(() => {document.getElementById('launch').disabled = false})
            .then(() => {chrome.storage.sync.get('coords').then((coords) => {map.setView(coords.coords, 1)})})
            .then(() => {chrome.storage.sync.get('intermediate').then((coord_list) => {if (coord_list.intermediate[0].length > 1) { for (coord of coord_list.intermediate[0]) {L.marker(coord).addTo(map)._icon.classList.add("huechange");}};})})
            .then(() => {chrome.storage.sync.get('coords').then((coords) => {L.marker(coords.coords).addTo(map).bindPopup("<b>Prediction</b><br>Here is the predicted point").openPopup()})})
            .then(() => {document.getElementById('validation').innerHTML = ''})
        }
    );

    document.getElementById('load').disabled = true;
    document.getElementById('launch').disabled = true;

}

async function open_maps() {

    const { coords } = await chrome.storage.sync.get('coords')
    window.open(`https://www.google.fr/maps?q= ${coords[0]}, ${coords[1]}`, '_blank', 'location=yes ,popup=yes')

}

async function guess() {
    
    function guess_location(lat, lng, token, game_type) {
        const xhr = new XMLHttpRequest();
        // post url is going to be the current game url
        const post_url = "https://www.geoguessr.com/api/v3/games/" + token;
        xhr.open("POST", post_url);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        
        // send lat, lng, and game url token in request
        xhr.send(JSON.stringify({"lng": lng, "lat": lat, "timedOut": false, "token": token}));
    }

    const { coords } = await chrome.storage.sync.get('coords');

    var lat = parseFloat(coords[0]);
    var long = parseFloat(coords[1]);

    chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
        
        const geo_url = tabs[0].url;
        url_as_list = geo_url.split('/');
    
        guess_location(lat, long, url_as_list[5], url_as_list[4]);

        localStorage.clear();
        chrome.runtime.sendMessage("reload");
        chrome.runtime.sendMessage("reset");
    });

}

async function autopin() {

    const { coords } = await chrome.storage.sync.get('coords');

    var lat = parseFloat(coords[0]);
    var long = parseFloat(coords[1]);

    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.scripting.executeScript({
            target : {tabId : tabs[0].id}, 
            files : ['autopin.js'],
        })
    });

    localStorage.clear();
    chrome.runtime.sendMessage("reset");
}

var load_btn = document.getElementById('load');
load_btn.addEventListener('click', get_screen);

var reset_btn = document.getElementById('reset');
reset_btn.addEventListener('click', reset);

var launch_btn = document.getElementById('launch');
launch_btn.addEventListener('click', compute_coords);

var open_btn = document.getElementById('display');
open_btn.addEventListener('click', open_maps);

var guess_btn = document.getElementById('submit');
guess_btn.addEventListener('click', guess);

//var autopin_btn = document.getElementById('autopin');
//autopin_btn.addEventListener('click', autopin);