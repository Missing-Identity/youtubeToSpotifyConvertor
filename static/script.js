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

function convertYouTubeToSpotify() {
  const youtubeUrl = document.getElementById("youtube-url").value;
  const resultDiv = document.getElementById("spotify-result");
  const artworkDiv = document.getElementById("youtube-artwork");

  showLoading("spotify-result");

  fetch("/api/youtube-to-spotify", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ youtube_url: youtubeUrl }),
  })
    .then((response) => response.json())
    .then((data) => {
      hideLoading("spotify-result");
      if (data.spotify_link) {
        if (data.spotify_link.startsWith("http")) {
          resultDiv.innerHTML = `<a href="${data.spotify_link}" target="_blank" class="spotify-link">Open in Spotify</a>`;
        } else {
          resultDiv.innerHTML = `<p>Spotify Link: ${data.spotify_link}</p>`;
        }
        resultDiv.className = "result slide-in";
        if (data.artwork_url) {
          artworkDiv.style.backgroundImage = `url(${data.artwork_url})`;
          artworkDiv.className = "artwork fade-in";
          setBackgroundCover(data.artwork_url);
        }
      } else {
        resultDiv.textContent = "Track not found on Spotify";
        resultDiv.className = "result slide-in";
        artworkDiv.style.backgroundImage = "none";
      }
    })
    .catch((error) => {
      hideLoading("spotify-result");
      resultDiv.textContent = "An error occurred";
      resultDiv.className = "result slide-in";
      artworkDiv.style.backgroundImage = "none";
      console.error("Error:", error);
    });
}

function convertSpotifyToYouTube() {
  const spotifyUrl = document.getElementById("spotify-url").value;
  const resultDiv = document.getElementById("youtube-result");
  const artworkDiv = document.getElementById("spotify-artwork");

  showLoading("youtube-result");

  fetch("/api/spotify-to-youtube", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ spotify_url: spotifyUrl }),
  })
    .then((response) => response.json())
    .then((data) => {
      hideLoading("youtube-result");
      if (data.youtube_music_link) {
        if (data.youtube_music_link.startsWith("http")) {
          resultDiv.innerHTML = `<a href="${data.youtube_music_link}" target="_blank" class="youtube-link">Open in YouTube Music</a>`;
        } else {
          resultDiv.innerHTML = `<p>YouTube Music Link: ${data.youtube_music_link}</p>`;
        }
        resultDiv.className = "result slide-in";
        if (data.artwork_url) {
          artworkDiv.style.backgroundImage = `url(${data.artwork_url})`;
          artworkDiv.className = "artwork fade-in";
          setBackgroundCover(data.artwork_url);
        }
      } else {
        resultDiv.textContent =
          data.error || "Track not found on YouTube Music";
        resultDiv.className = "result slide-in";
        artworkDiv.style.backgroundImage = "none";
      }
    })
    .catch((error) => {
      hideLoading("youtube-result");
      resultDiv.textContent = "An error occurred";
      resultDiv.className = "result slide-in";
      artworkDiv.style.backgroundImage = "none";
      console.error("Error:", error);
    });
}
