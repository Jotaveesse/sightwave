var inputField;
var textArea;

window.onload = function(){
    inputField = document.getElementById('input-field');
    textArea = document.getElementById('text-area');
};

function requestLyricsFromLyrics() {
    const apiUrl = 'https://image-to-lyrics.vercel.app/api';

    const searchPrompt = inputField.value;

    fetch(`${apiUrl}?search_prompt=${encodeURIComponent(searchPrompt)}`)
    .then(response => response.json())
    .then(data => {
        textArea.value = '';
        data.tracks.forEach(element => {
            if (element != null)
                textArea.value += element.matched_section + '\n';
        });
        
    })
    .catch(error => {
        console.error('Error:', error);
        textArea.value = 'An error occurred while fetching lyrics.';
    });
}

function requestLyricsFromImage() {
    const apiUrl = 'https://image-to-lyrics.vercel.app/api';

    const searchPrompt = inputField.value;

    fetch(`${apiUrl}?url=${encodeURIComponent(searchPrompt)}`)
    .then(response => response.json())
    .then(data => {
        textArea.value = '';
        data.tracks.forEach(element => {
            if (element != null)
                textArea.value += element.matched_section + '\n';
        });
        
    })
    .catch(error => {
        console.error('Error:', error);
        textArea.value = 'An error occurred while fetching lyrics.';
    });
}