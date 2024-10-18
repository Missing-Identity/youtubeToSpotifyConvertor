import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
import yt_dlp
from spotipy.exceptions import SpotifyException
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Spotify API credentials
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

print(f"Client ID: {SPOTIPY_CLIENT_ID[:5]}...") # Print first 5 characters for verification
print(f"Client Secret: {SPOTIPY_CLIENT_SECRET[:5]}...") # Print first 5 characters for verification

try:
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET
    ))
except Exception as e:
    print(f"Error initializing Spotify client: {e}")
    spotify = None

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def spotify_to_youtube(spotify_url):
    """
    Convert Spotify track link to YouTube and YouTube Music video links.
    """
    if not spotify:
        print("Spotify client not initialized")
        return None, None, None

    # Extract the track ID from the Spotify URL, ignoring query parameters
    track_id = spotify_url.split('/')[-1].split('?')[0]
    
    try:
        # Retrieve the track information using the correct track ID
        track_info = spotify.track(track_id)
        track_name = track_info['name']
        artist_name = track_info['artists'][0]['name']
        
        # Search for YouTube video
        request = youtube.search().list(q=f"{track_name} {artist_name}", part='snippet', type='video', maxResults=1)
        response = request.execute()
        
        # Check if a result was found
        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            youtube_link = f"https://www.youtube.com/watch?v={video_id}"
            youtube_music_link = f"https://music.youtube.com/watch?v={video_id}"
            return youtube_link, youtube_music_link, track_info
        else:
            return None, None, None
    except SpotifyException as e:
        print(f"Spotify API error: {e}")
        return None, None, None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None, None

# Add this function to the existing file
def get_spotify_track_info(spotify_url):
    if not spotify:
        print("Spotify client not initialized")
        return None

    track_id = spotify_url.split('/')[-1].split('?')[0]
    try:
        return spotify.track(track_id)
    except SpotifyException as e:
        print(f"Spotify API error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
