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

PLACEHOLDER_ARTWORK = "https://th.bing.com/th/id/OIP.3J7PcVZf3uIt04PUYAvMTwHaHa?rs=1&pid=ImgDetMain"  # Replace with an actual placeholder image URL

def get_youtube_metadata(youtube_url):
    """
    Extract metadata from YouTube Music video using yt-dlp.
    """
    ydl_opts = {}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            title = info.get('title', None)
            artist = info.get('artist', None)
            artwork_url = info.get('thumbnail', PLACEHOLDER_ARTWORK)
            return title, artist, artwork_url
    except Exception as e:
        print(f"Error extracting YouTube metadata: {str(e)}")
        return None, None, PLACEHOLDER_ARTWORK

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
    title, artist, artwork_url = get_youtube_metadata(youtube_url)
    if title:
        spotify_link = search_spotify_track(title, artist)
        return spotify_link, artwork_url
    else:
        return None, PLACEHOLDER_ARTWORK
