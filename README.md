# Music Platform Converter

Music Platform Converter is a web application that allows users to convert music links between Spotify and YouTube/YouTube Music. It provides a simple interface for users to input a link from one platform and get the corresponding link on the other platform.

## Features

- Convert YouTube/YouTube Music links to Spotify
- Convert Spotify links to YouTube and YouTube Music
- Display album artwork for converted tracks
- Simple and intuitive user interface

## Technologies Used

- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- APIs: Spotify API, YouTube Data API
- Other libraries: spotipy, yt-dlp, google-api-python-client

## Setup

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/music-platform-converter.git
   cd music-platform-converter
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory and add the following:

   ```
   SPOTIPY_CLIENT_ID=your_spotify_client_id
   SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
   YOUTUBE_API_KEY=your_youtube_api_key
   ```

4. Run the application:

   ```
   python app.py
   ```

5. Open a web browser and navigate to `http://localhost:5000` to use the application.

## Usage

1. Choose the conversion direction (YouTube to Spotify or Spotify to YouTube).
2. Enter the URL of the track you want to convert.
3. Click the "Convert" button.
4. The application will display the converted link and album artwork.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [Flask](https://flask.palletsprojects.com/)
- [spotipy](https://spotipy.readthedocs.io/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
