var inputField;
var textArea;
var embedTemplate;
var imageUpload;
var imageUploadTop;
var imageInput;
var imageDisplayArea;
var imageDisplay;
var sendAnotherButton;
var imageSendButton;
var urlInput;
var fileDropArea;
var sendButton;
var lyricsText;
var embedSection;
var buttonArea;
var loadingArea;

var currUrl = null;
var currFile = null;

//const apiUrl = window.location.href + 'api/search/';
const apiUrl = 'https://image-to-lyrics.vercel.app/api/search/'

window.onload = function () {
    inputField = document.getElementById('input-field');
    textArea = document.getElementById('text-area');
    embedTemplate = document.getElementById('embed-iframe-template');
    imageUpload = document.getElementById('image-upload');
    imageUploadTop = document.getElementById('image-upload-top');
    imageInput = document.getElementById('image-input');
    imageDisplayArea = document.getElementById('image-display-area');
    imageDisplay = document.getElementById('image-display');
    sendAnotherButton = document.getElementById('send-another-button');
    fileDropArea = document.getElementById('file_drop_area');
    imageSendButton = document.getElementById('url-send-button');
    sendButton = document.getElementById('end-button');
    urlInput = document.getElementById('url-input').children[0];
    lyricsText = document.getElementById('lyrics-text');
    embedSection = document.getElementById('embed-section');
    buttonArea = document.getElementById('button-area');
    loadingArea = document.getElementById('loading-area');

    imageUpload.addEventListener('dragover', function (e) {
        e.preventDefault();
    });

    imageUploadTop.addEventListener('dragenter', function (e) {
        e.preventDefault();
        var children = imageUploadTop.children;
        for (const child of children) {
            child.classList.add('brightened');
        }

    });

    imageUploadTop.addEventListener('dragleave', function (e) {
        e.preventDefault();
        var children = imageUploadTop.children;
        for (const child of children) {
            child.classList.remove('brightened');
        }
    });

    imageUploadTop.addEventListener('drop', function (e) {
        e.preventDefault();

        const files = e.dataTransfer.files;
        handleFiles(files);
    });

    sendAnotherButton.addEventListener('click', function (e) {
        currUrl = null;
        toggleVisibility(imageDisplay);
        toggleVisibility(imageUpload);
    });

    imageSendButton.addEventListener('click', function (e) {
        isImageURLValid(urlInput.value, function (isValid) {
            if (isValid) {
                currUrl = urlInput.value;
                imageDisplayArea.src = currUrl;
                toggleVisibility(imageDisplay);
                toggleVisibility(imageUpload);
            } else {
                alert('URL inválida');
            }
        });
    });


    // Function to handle dropped files
    function handleFiles(files) {
        if (files && files[0]) {
            const selectedFile = files[0];

            const reader = new FileReader();

            reader.onload = function (event) {
                imageDisplayArea.src = event.target.result;
                toggleVisibility(imageDisplay);
                toggleVisibility(imageUpload);
            }

            // Read the selected file as a data URL
            reader.readAsDataURL(selectedFile);
        }
    }
};

function isImageURLValid(url, callback) {
    var img = new Image();
    img.onload = function () {
        callback(true);
    };
    img.onerror = function () {
        callback(false);
    };
    img.src = url;
}

function toggleVisibility(element) {
    element.classList.toggle('hidden');
}

function createEmbed(trackId) {
    var embed = embedTemplate.content.cloneNode(true);
    var clonedIframe = embed.querySelector('iframe');
    clonedIframe.src = clonedIframe.src.replace('TRACKID', trackId)

    embedSection.appendChild(clonedIframe);
}

function requestLyricsFromImage() {
    if (currUrl == null)
        return;

    queryParams = {
        url: inputField.value
    }
    /*getRequest(apiUrl+'image', queryParams).then(data => {
        displayTracks([data]);

    }).catch(error => {
        textArea.value = 'An error occurred while fetching lyrics: ' + error;
    });*/
}

function requestLyricsFromLyrics() {
    //if (currUrl == null)
    //    return;

    queryParams = {
        query: urlInput.value
    }

    toggleVisibility(loadingArea)
    toggleVisibility(buttonArea)
    getRequest(apiUrl + 'lyrics', queryParams).then(data => {
        toggleVisibility(loadingArea)
        toggleVisibility(buttonArea)
        displayTracks([data]);

    }).catch(error => {
        lyricsText.innerHTML = 'An error occurred while fetching lyrics: ' + error;
    });
}

function requestLyricsFromFeats() {
    if (currUrl == null)
        return;

    queryParams = {
        query: inputField.value
    }
    getRequest(apiUrl + 'features', queryParams).then(data => {
        displayTracks([data]);

    }).catch(error => {
        lyricsText.innerHTML = 'An error occurred while fetching lyrics: ' + error;
    });
}

function displayTracks(tracks) {
    var iframes = Array.from(document.getElementsByClassName('embed-iframe'));
    iframes.forEach(element => {
        element.remove();
    });

    lyricsText.value = '';

    console.log(tracks);

    tracks.forEach(element => {

        if (element != null) {
            createEmbed(element.id);
            console.log(element);
            lyricsText.innerHTML += element.lyrics.join("<br>");
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
