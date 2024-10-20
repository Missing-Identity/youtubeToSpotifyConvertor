function showLoading(elementId) {
  const element = document.getElementById(elementId);
  element.innerHTML = '<div class="loading"></div>';
}

function hideLoading(elementId) {
  const element = document.getElementById(elementId);
  element.innerHTML = "";
}

function setBackgroundCover(imageUrl) {
  const backgroundCover = document.querySelector(".background-cover");
  if (!backgroundCover) {
    const newBackgroundCover = document.createElement("div");
    newBackgroundCover.className = "background-cover";
    document.body.appendChild(newBackgroundCover);
  }
  document.querySelector(
    ".background-cover"
  ).style.backgroundImage = `url(${imageUrl})`;
}

function convertLink() {
  const musicUrl = document.getElementById("music-url").value;
  const resultDiv = document.getElementById("result");
  const artworkDiv = document.getElementById("artwork");
  const convertButton = document.getElementById("convert-button");

  showLoading("result");

  let apiEndpoint = "";
  let sourceType = "";

  if (musicUrl.includes("youtube.com") || musicUrl.includes("youtu.be")) {
    apiEndpoint = "/api/youtube-to-spotify";
    sourceType = "youtube";
  } else if (musicUrl.includes("spotify.com")) {
    apiEndpoint = "/api/spotify-to-youtube";
    sourceType = "spotify";
  } else {
    resultDiv.textContent =
      "Invalid URL. Please enter a valid YouTube or Spotify link.";
    return;
  }

  fetch(apiEndpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url: musicUrl }),
  })
    .then((response) => response.json())
    .then((data) => {
      hideLoading("result");
      if (data.converted_link) {
        const targetType = sourceType === "youtube" ? "spotify" : "youtube";
        const buttonClass = `${targetType}-link`;
        const buttonText = `Open in ${
          targetType.charAt(0).toUpperCase() + targetType.slice(1)
        }`;

        resultDiv.innerHTML = `
          <a href="${data.converted_link}" target="_blank" class="${buttonClass}">${buttonText}</a>
          <a href="/player?id=${data.track_id}&source=${targetType}" class="${buttonClass}">Play Preview</a>
        `;
        resultDiv.className = "result slide-in";
        if (data.artwork_url) {
          artworkDiv.style.backgroundImage = `url(${data.artwork_url})`;
          artworkDiv.className = "artwork fade-in";
          setBackgroundCover(data.artwork_url);
        }
        convertButton.className =
          sourceType === "youtube" ? "spotify-button" : "youtube-button";
      } else {
        resultDiv.textContent = data.error || "Conversion failed";
        resultDiv.className = "result slide-in";
        artworkDiv.style.backgroundImage = "none";
      }
    })
    .catch((error) => {
      hideLoading("result");
      resultDiv.textContent = "An error occurred";
      resultDiv.className = "result slide-in";
      artworkDiv.style.backgroundImage = "none";
      console.error("Error:", error);
    });
}
