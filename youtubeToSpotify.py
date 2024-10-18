import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

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

PLACEHOLDER_ARTWORK = "https://th.bing.com/th/id/OIP.3J7PcVZf3uIt04PUYAvMTwHaHa?rs=1&pid=ImgDetMain"

def get_youtube_metadata(youtube_url):
    """
    Extract metadata from YouTube video using YouTube Data API.
    """
    try:
        # Extract video ID from URL
        parsed_url = urlparse(youtube_url)
        video_id = parse_qs(parsed_url.query).get('v', [None])[0]
        if not video_id:
            video_id = parsed_url.path.split('/')[-1]

        # Get video details
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()

        if 'items' in response and len(response['items']) > 0:
            snippet = response['items'][0]['snippet']
            title = snippet['title']
            channel_title = snippet['channelTitle']
            thumbnail = snippet['thumbnails']['high']['url']
            return title, channel_title, thumbnail
        else:
            print("No items found in YouTube response")
            return None, None, PLACEHOLDER_ARTWORK
    except Exception as e:
        print(f"Error extracting YouTube metadata: {str(e)}")
        return None, None, PLACEHOLDER_ARTWORK

def search_spotify_track(track_name, artist_name=None):
    """
    Search for the song on Spotify using the track name and artist.
    """
    try:
        query = f"{track_name}"
        if artist_name:
            query += f" artist:{artist_name}"
        
        results = spotify.search(q=query, type='track', limit=1)
        
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            return track['external_urls']['spotify'], track['album']['images'][0]['url']
        else:
            print(f"No Spotify results for query: {query}")
            return None, None
    except Exception as e:
        print(f"Error searching Spotify: {str(e)}")
        return None, None

def youtube_to_spotify(youtube_url):
    """
    Convert YouTube Music video link to Spotify track link.
    """
    title, artist, yt_thumbnail = get_youtube_metadata(youtube_url)
    if title:
        print(f"Searching Spotify for: {title} by {artist}")
        spotify_link, spotify_artwork = search_spotify_track(title, artist)
        if spotify_link:
            return spotify_link, spotify_artwork or yt_thumbnail
        else:
            print("Track not found on Spotify, trying without artist name")
            spotify_link, spotify_artwork = search_spotify_track(title)
            if spotify_link:
                return spotify_link, spotify_artwork or yt_thumbnail
    
    print("Unable to find matching track on Spotify")
    return None, yt_thumbnail
