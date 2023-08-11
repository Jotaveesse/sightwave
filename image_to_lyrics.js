function requestLyrics() {
    const inputField = document.getElementById('input-field');
    const textArea = document.getElementById('text-area');

    const apiUrl = 'https://image-to-lyrics.vercel.app/api';

    const searchPrompt = inputField.value;

    // Make a GET request to the API
    fetch(`${apiUrl}?search_prompt=${encodeURIComponent(searchPrompt)}`)
    .then(response => response.json())
    .then(data => {
        // Update the text area with the result from the API
        textArea.value = data;
    })
    .catch(error => {
        console.error('Error:', error);
        textArea.value = 'An error occurred while fetching lyrics.';
    });
}