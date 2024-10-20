document.addEventListener("DOMContentLoaded", function () {
  const urlParams = new URLSearchParams(window.location.search);
  const trackId = urlParams.get("id");
  const source = urlParams.get("source");

  const playerContainer = document.querySelector(".player-container");
  playerContainer.classList.add(`${source}-theme`);

  fetch(`/api/track-info?id=${trackId}&source=${source}`)
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("title").textContent = data.title;
      document.getElementById("artist").textContent = data.artist;
      document.getElementById("album").textContent = data.album;
      document.getElementById(
        "artwork"
      ).style.backgroundImage = `url(${data.artwork_url})`;
      setBackgroundCover(data.artwork_url);

      if (source === "spotify") {
        const audioPlayer = document.getElementById("audio-player");
        audioPlayer.src = data.preview_url;
        audioPlayer.style.display = "block";
        document.getElementById("youtube-player").style.display = "none";
      } else if (source === "youtube") {
        const youtubePlayer = document.getElementById("youtube-player");
        youtubePlayer.src = data.preview_url;
        youtubePlayer.style.display = "block";
        document.getElementById("audio-player").style.display = "none";
      }
    })
    .catch((error) => console.error("Error:", error));

  const loopButton = document.getElementById("loop-button");
  const audioPlayer = document.getElementById("audio-player");

  loopButton.addEventListener("click", function () {
    if (source === "spotify") {
      audioPlayer.loop = !audioPlayer.loop;
      this.textContent = audioPlayer.loop ? "Unloop" : "Loop";
    } else if (source === "youtube") {
      alert("Looping is not available for YouTube previews");
    }
  });
});

function setBackgroundCover(imageUrl) {
  const backgroundCover = document.querySelector(".background-cover");
  if (!backgroundCover) {
    const newBackgroundCover = document.createElement("div");
    newBackgroundCover.className = "background-cover";
    document.body.appendChild(newBackgroundCover);
  }
  backgroundCover.style.backgroundImage = `url(${imageUrl})`;
}
