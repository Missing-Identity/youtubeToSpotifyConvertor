from flask import Flask, request, jsonify, render_template, redirect, url_for
from youtubeToSpotify import youtube_to_spotify
from spotifyToYoutube import spotify_to_youtube, get_spotify_track_info
from googleapiclient.discovery import build
import os
import traceback

app = Flask(__name__)

# Initialize YouTube API
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/youtube-to-spotify', methods=['POST'])
def api_youtube_to_spotify():
    youtube_url = request.json['url']
    spotify_link, artwork_url = youtube_to_spotify(youtube_url)
    if spotify_link:
        track_id = spotify_link.split('/')[-1].split('?')[0]
        return jsonify({
            'converted_link': spotify_link,
            'artwork_url': artwork_url,
            'track_id': track_id
        })
    else:
        return jsonify({'error': 'Track not found on Spotify'}), 404

@app.route('/api/spotify-to-youtube', methods=['POST'])
def api_spotify_to_youtube():
    spotify_url = request.json['url']
    youtube_link, youtube_music_link, track_info = spotify_to_youtube(spotify_url)
    if youtube_music_link:
        track_id = youtube_music_link.split('v=')[1]
        return jsonify({
            'converted_link': youtube_music_link,
            'artwork_url': track_info['album']['images'][0]['url'] if track_info['album']['images'] else None,
            'track_id': track_id
        })
    else:
        return jsonify({'error': 'Track not found on YouTube Music'}), 404

@app.route('/player')
def player():
    track_id = request.args.get('id')
    source = request.args.get('source')
    return render_template('player.html', track_id=track_id, source=source)

@app.route('/api/track-info', methods=['GET'])
def get_track_info():
    track_id = request.args.get('id')
    source = request.args.get('source')
    
    if source == 'spotify':
        track_info = get_spotify_track_info(f"https://open.spotify.com/track/{track_id}")
        if track_info:
            return jsonify({
                'title': track_info['name'],
                'artist': track_info['artists'][0]['name'],
                'album': track_info['album']['name'],
                'artwork_url': track_info['album']['images'][0]['url'],
                'preview_url': track_info['preview_url']
            })
    elif source == 'youtube':
        try:
            youtube_request = youtube.videos().list(
                part="snippet",
                id=track_id
            )
            response = youtube_request.execute()

            if 'items' in response and len(response['items']) > 0:
                video_info = response['items'][0]['snippet']
                return jsonify({
                    'title': video_info['title'],
                    'artist': video_info['channelTitle'],
                    'album': 'N/A',  # YouTube videos don't have album info
                    'artwork_url': video_info['thumbnails']['high']['url'],
                    'preview_url': f"https://www.youtube.com/embed/{track_id}"  # Use embed URL for preview
                })
        except Exception as e:
            print(f"Error retrieving YouTube track info: {str(e)}")
    
    return jsonify({'error': 'Track information not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
