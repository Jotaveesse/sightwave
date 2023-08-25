var inputField;
var textArea;
var embedTemplate;
const apiUrl = 'https://image-to-lyrics.vercel.app/api/search/';

window.onload = function () {
    inputField = document.getElementById('input-field');
    textArea = document.getElementById('text-area');
    embedTemplate = document.getElementById('embed-iframe-template');
};

function createEmbed(trackId) {
    var embed = embedTemplate.content.cloneNode(true);
    var clonedIframe = embed.querySelector('iframe');
    clonedIframe.src =  clonedIframe.src.replace('TRACKID', trackId)
    
    document.body.appendChild(clonedIframe);
}

function requestLyricsFromImage() {
    queryParams = {
        url: inputField.value
    }
    getRequest(apiUrl+'image', queryParams).then(data => {
        displayTracks(data.tracks);

    }).catch(error => {
        textArea.value = 'An error occurred while fetching lyrics: ' + error;
    });
}

function requestLyricsFromLyrics() {
    queryParams = {
        search_prompt:  inputField.value
    }
    getRequest(apiUrl+'lyrics', queryParams).then(data => {
        displayTracks(data.tracks);
        
    }).catch(error => {
        textArea.value = 'An error occurred while fetching lyrics: ' + error;
    });
}

function requestLyricsFromFeats(){
    queryParams = {
        search_prompt:  inputField.value
    }
    getRequest(apiUrl+'features', queryParams).then(data => {
        displayTracks(data.tracks);
        
    }).catch(error => {
        textArea.value = 'An error occurred while fetching lyrics: ' + error;
    });
}

function displayTracks(tracks) {
    var iframes = Array.from(document.getElementsByClassName('embed-iframe'));
    iframes.forEach(element => {
        element.remove();
    });
    
    textArea.value = '';
    
    console.log(tracks);

    tracks.forEach(element => {

        if (element != null) {
            createEmbed(element.id);
            textArea.value += element.matched_section + '\n';
        }
    });
}

function getRequest(url, queryParams = {}) {
    const queryString = Object.keys(queryParams)
        .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(queryParams[key])}`)
        .join('&');

    const fullUrl = queryString ? `${url}?${queryString}` : url;

    return fetch(fullUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.status} ${response.statusText}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('Error making GET request:', error);
            throw error;
        });
}
