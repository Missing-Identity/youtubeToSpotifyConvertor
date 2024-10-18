import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
import yt_dlp
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Spotify API credentials
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))

# Initialize YouTube API
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


def get_youtube_metadata(youtube_url):
    """
    Extract metadata from YouTube Music video using yt-dlp.
    """
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        title = info.get('title', None)
        artist = info.get('artist', None)
        artwork_url = info.get('thumbnail', None)
        return title, artist, artwork_url


def search_spotify_track(track_name, artist_name=None):
    """
    Search for the song on Spotify using the track name and artist.
    """
    query = track_name
    if artist_name:
        query += f" artist:{artist_name}"
    results = spotify.search(q=query, type='track', limit=1)
    if results['tracks']['items']:
        return results['tracks']['items'][0]['external_urls']['spotify']
    else:
        return None


def youtube_to_spotify(youtube_url):
    """
    Convert YouTube Music video link to Spotify track link.
    """
    # Adjust the unpacking to match the number of returned values
    title, artist, _ = get_youtube_metadata(youtube_url)  # Ignore artwork_url if not needed
    if title:
        spotify_link = search_spotify_track(title, artist)
        if spotify_link:
            return spotify_link
        else:
            return None
    else:
        return None
