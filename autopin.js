function placeMarker(){

    lat = -4.0;
    lng = 2.0;

    let element = document.getElementsByClassName("guess-map__canvas-container")[0] // html element containing needed props.
    let keys = Object.keys(element) // all keys
    let key = keys.find(key => key.startsWith("__reactFiber$")) // the React key I need to access props
    let placeMarker = element[key].return.memoizedProps.onMarkerLocationChanged // getting the function which will allow me to place a marker on the map

    placeMarker({lat:lat,lng:lng}) // placing the marker on the map at the correct coordinates given by getCoordinates(). Must be passed as an Object.
}

setTimeout(() => {placeMarker();}, 250);