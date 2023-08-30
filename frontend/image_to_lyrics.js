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
var openFileButton;
var fileInput;

var currUrl = null;
var currImage = null;

const apiUrl = window.location.href + 'api/search/';
//const apiUrl = 'https://image-to-lyrics.vercel.app/api/search/'

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
    openFileButton = document.getElementById('select_file_button');
    fileInput = document.getElementById('file-input');

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
        currImage = null;
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
            }
            else {
                alert('URL inválida');
            }
        });
    });

    openFileButton.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', () => {
        handleFiles(fileInput.files);
    });


};
// Function to handle dropped files
function handleFiles(files) {
    if (files && files[0]) {
        const selectedFile = files[0];

        const reader = new FileReader();

        reader.onload = function (event) {
            imageDisplayArea.src = reader.result;
            toggleVisibility(imageDisplay);
            toggleVisibility(imageUpload);
        }

        reader.onloadend = function () {
            currImage = reader.result;
        }

        // Read the selected file as a data URL
        imgBase64 = reader.readAsDataURL(selectedFile);
        console.log(imgBase64);
    }
}

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

function searchLiteral() {
    if (currUrl != null) {
        toggleVisibility(loadingArea)
        toggleVisibility(buttonArea)
        
        queryParams = {
            url: currUrl
        }

        getRequest(apiUrl + 'both', queryParams).then(data => {
            displayTracks([data]);
            
        }).catch(error => {
            lyricsText.innerHTML = 'Erro: ' + error;
            
        }).finally(() => {
            toggleVisibility(loadingArea)
            toggleVisibility(buttonArea)
        });
    }
    else if (currImage != null) {
        toggleVisibility(loadingArea)
        toggleVisibility(buttonArea)
        
        bodyParams={
            image : currImage
        }

        postRequest(apiUrl + 'literal', bodyParams).then(data => {
            displayTracks([data]);
            
        }).catch(error => {
            lyricsText.innerHTML = 'Erro: ' + error;

        }).finally(() => {
            toggleVisibility(loadingArea)
            toggleVisibility(buttonArea)
        });
    }
}

function searchEmotional() {
    if (currUrl != null) {
        toggleVisibility(loadingArea)
        toggleVisibility(buttonArea)
        
        queryParams = {
            url: currUrl
        }

        getRequest(apiUrl + 'emotional', queryParams).then(data => {
            displayTracks([data]);
            
        }).catch(error => {
            lyricsText.innerHTML = 'Erro: ' + error;
            
        }).finally(() => {
            toggleVisibility(loadingArea)
            toggleVisibility(buttonArea)
        });
    }
    else if (currImage != null) {
        toggleVisibility(loadingArea)
        toggleVisibility(buttonArea)
        
        bodyParams={
            image : currImage
        }

        postRequest(apiUrl + 'both', bodyParams).then(data => {
            displayTracks([data]);
            
        }).catch(error => {
            lyricsText.innerHTML = 'Erro: ' + error;

        }).finally(() => {
            toggleVisibility(loadingArea)
            toggleVisibility(buttonArea)
        });
    }
}

function searchBoth() {
    if (currUrl != null) {
        toggleVisibility(loadingArea)
        toggleVisibility(buttonArea)
        
        queryParams = {
            url: currUrl
        }

        getRequest(apiUrl + 'both', queryParams).then(data => {
            displayTracks([data]);
            
        }).catch(error => {
            lyricsText.innerHTML = 'Erro: ' + error;
            
        }).finally(() => {
            toggleVisibility(loadingArea)
            toggleVisibility(buttonArea)
        });
    }
    else if (currImage != null) {
        toggleVisibility(loadingArea)
        toggleVisibility(buttonArea)
        
        bodyParams={
            image : currImage
        }

        postRequest(apiUrl + 'both', bodyParams).then(data => {
            displayTracks([data]);
            
        }).catch(error => {
            lyricsText.innerHTML = 'Erro: ' + error;

        }).finally(() => {
            toggleVisibility(loadingArea)
            toggleVisibility(buttonArea)
        });
    }
}

function displayTracks(tracks) {
    var iframes = Array.from(document.getElementsByClassName('embed-iframe'));
    iframes.forEach(element => {
        element.remove();
    });

    lyricsText.innerHTML = '';

    tracks.forEach(track => {

        if (track != null) {
            createEmbed(track.id);
            console.log(track);

            for (var i = 0; i < track.lyrics.length; i++) {
                if (i >= track.matched_section_id && i <= track.matched_section_id + 2) {
                    lyricsText.innerHTML += `<div style="background-color:#661144">${track.lyrics[i]}</div>`;
                }
                else
                    lyricsText.innerHTML += `<div>${track.lyrics[i]}</div>`;
            }
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

function postRequest(url, body = {}, queryParams = {}) {
    const queryString = Object.keys(queryParams)
        .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(queryParams[key])}`)
        .join('&');

    const fullUrl = queryString ? `${url}?${queryString}` : url;

    return fetch(fullUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.status} ${response.statusText}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('Error making POST request:', error);
            throw error;
        });
}
