var imageUpload,
  imageUploadTop,
  imageDisplay,
  imageInput,
  urlInput,
  fileInput,
  imageDisplayArea,
  fileDropArea,
  buttonArea,
  loadingArea,
  sendButton,
  sendAnotherButton,
  imageSendButton,
  openFileButton,
  embedSection,
  embedTemplate,
  sliderValue;

var currUrl = null;
var currImage = null;
var trackAmount = 1;

const apiUrl = window.location.origin + "/api/search/";
//const apiUrl = 'https://image-to-lyrics.vercel.app/api/search/'

window.onload = function () {
  imageUpload = document.getElementById("image-upload");
  imageUploadTop = document.getElementById("image-upload-top");
  imageDisplay = document.getElementById("image-display");

  imageInput = document.getElementById("image-input");
  urlInput = document.getElementById("url-input").children[0];
  fileInput = document.getElementById("file-input");

  suggestionAmount = document.getElementById("amount-of-suggestions");

  imageDisplayArea = document.getElementById("image-display-area");
  fileDropArea = document.getElementById("file_drop_area");
  buttonArea = document.getElementById("button-area");
  loadingArea = document.getElementById("loading-area");
  trackSection = document.getElementById("track-section");

  sendButton = document.getElementById("end-button");
  sendAnotherButton = document.getElementById("send-another-button");
  imageSendButton = document.getElementById("url-send-button");
  openFileButton = document.getElementById("select_file_button");

  embedTemplate = document.getElementById("embed-iframe-template");
  embedSection = document.getElementById("embed-section");

  sliderValue = document.getElementById("slider-value");

  imageUpload.addEventListener("dragover", function (e) {
    e.preventDefault();
  });

  // deixa o componente mais claro quando tem algum arquivo sendo arrastado
  imageUploadTop.addEventListener("dragenter", function (e) {
    e.preventDefault();
    const children = imageUploadTop.children;
    for (const child of children) {
      child.classList.add("brightened");
    }
  });

  // tira a claridade
  imageUploadTop.addEventListener("dragleave", function (e) {
    e.preventDefault();
    const children = imageUploadTop.children;
    for (const child of children) {
      child.classList.remove("brightened");
    }
  });

  //recebe o arquivo
  imageUploadTop.addEventListener("drop", function (e) {
    e.preventDefault();
    const files = e.dataTransfer.files;

    handleFiles(files);
  });

  //reseta os valores da imagem selecionada
  sendAnotherButton.addEventListener("click", function (e) {
    currUrl = null;
    currImage = null;
    toggleVisibility(imageDisplay);
    toggleVisibility(imageUpload);
  });

  //carrega a imagem a partir da url
  imageSendButton.addEventListener("click", function (e) {
    isImageURLValid(urlInput.value, function (isValid) {
      if (isValid) {
        currUrl = urlInput.value;
        imageDisplayArea.src = currUrl;

        toggleVisibility(imageDisplay);
        toggleVisibility(imageUpload);
      } else {
        alert("URL inválida");
      }
    });
  });

  //quando clica botao de escolher arquivo
  openFileButton.addEventListener("click", () => {
    fileInput.click();
  });

  //quando recebe um arquivo
  fileInput.addEventListener("change", () => {
    handleFiles(fileInput.files);
  });
};

var IFrameAPI;
window.onSpotifyIframeApiReady = (API) => {
  IFrameAPI = API;
  // createIFrame("2enPRFda84VE2wtI8c86Uf")
};

//pesquisa por uma musica usando a api
function searchTrack(searchOption) {
  if (currUrl !== null || currImage !== null) {
    toggleVisibility(loadingArea);
    toggleVisibility(buttonArea);
    toggleVisibility(trackSection, false)

    let requestPromise;
    let params;

    if (currUrl !== null) {
      params = {
        url: currUrl,
        amount: trackAmount,
      };
      requestPromise = getRequest(apiUrl + searchOption, params);
    } else {
      body = {
        image: currImage,
      };
      params = {
        amount: trackAmount,
      };
      requestPromise = postRequest(apiUrl + searchOption, body, params);
    }

    requestPromise
      .then((data) => {
        console.log(data);
        displayTracks(data);
      })
      .catch((error) => {
        alert("Error: " + error);
      })
      .finally(() => {
        toggleVisibility(loadingArea);
        toggleVisibility(buttonArea);
        toggleVisibility(trackSection, true)

        trackSection.scrollIntoView({
          behavior: "smooth", // Use smooth scrolling animation
          block: "start", // Scroll to the top of the element
          inline: "nearest",
        });
      });
  }
}

//exibe a musica
function displayTracks(tracks) {
  var iframes = Array.from(document.getElementsByClassName("track-elem"));
  iframes.forEach((element) => {
    element.remove();
  });

  tracks.forEach((track) => {
    if (track != null) {
      console.log(track);

      var createdEmbed = createEmbed(track.id);
      var lyricsText = createdEmbed.getElementsByClassName("lyrics-text")[0];

      lyricsText.innerHTML = "";

      //para cada pedaço da letra
      for (var i = 0; i < track.lyrics.length; i++) {
        var hasMatchedSection = track.matched_section_id != -1;
        var isMatchedSection =
          i >= track.matched_section_id && i <= track.matched_section_id + 2;

        //colocar uma cor diferente na parte da letra que deu match
        if (hasMatchedSection && isMatchedSection) {
          lyricsText.innerHTML += `<div style="background-color:#661144">${track.lyrics[i]}</div>`;
        } else lyricsText.innerHTML += `<div>${track.lyrics[i]}</div>`;
      }
    }
  });
}

//cria o embed to spotify
function createEmbed(trackId) {
  var embed = embedTemplate.content.cloneNode(true);
  var lyricsSection = embed.querySelector(".lyrics-section");
  var clonedIframe = embed.querySelector("iframe");
  embedSection.appendChild(embed);


  const options = {
    class: "embed-iframe",
    style: "border-radius: 120px; background-color:#333",
    width: '100%',
    height: '154px',
    uri: 'spotify:track:' + trackId
  };

  const callback = (embedController) => {
    embedController.addListener('playback_update', e => {
      console.log(e);
      toggleVisibility(lyricsSection, !e.data.isPaused);
    });


  };
  IFrameAPI.createController(clonedIframe, options, callback);

  return lyricsSection;
}

// pega o arquivo e armazena como base64
function handleFiles(files) {
  if (files && files[0]) {
    const selectedFile = files[0];

    const reader = new FileReader();

    reader.onloadend = function () {
      currImage = reader.result;
      imageDisplayArea.src = reader.result;

      toggleVisibility(imageDisplay);
      toggleVisibility(imageUpload);
    };

    reader.readAsDataURL(selectedFile);
  }
}

//checa se é uma url valida de imagem
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

//esconde ou mostra o componente escolhido
function toggleVisibility(element, visible = null) {
  if (visible == null)
    element.classList.toggle("hidden");
  else {
    if (visible)
      element.classList.remove("hidden");
    else
      element.classList.add("hidden");
  }
}

//changes the value of amount based on the user input
function changeAmount() {
  const possibleAmount = suggestionAmount.value;
  if (
    isNaN(possibleAmount) ||
    Number(possibleAmount) > 8 ||
    Number(possibleAmount) < 1
  ) {
    alert("Insira um número entre 1 e 8");
    return;
  }
  trackAmount = suggestionAmount.value;
  sliderValue.textContent = "Buscar " + trackAmount + (trackAmount == 1 ? " Música" : " Músicas");
}
