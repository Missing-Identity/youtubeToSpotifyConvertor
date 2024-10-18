from flask import Flask, request, jsonify, render_template
from youtubeToSpotify import youtube_to_spotify
from spotifyToYoutube import spotify_to_youtube, get_spotify_track_info
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/youtube-to-spotify', methods=['POST'])
def api_youtube_to_spotify():
    youtube_url = request.json['youtube_url']
    try:
        spotify_link, artwork_url = youtube_to_spotify(youtube_url)
        if spotify_link:
            return jsonify({
                'spotify_link': spotify_link,
                'artwork_url': artwork_url
            })
        else:
            return jsonify({'error': 'Track not found on Spotify'}), 404
    except Exception as e:
        print(f"Error in api_youtube_to_spotify: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/api/spotify-to-youtube', methods=['POST'])
def api_spotify_to_youtube():
    spotify_url = request.json['spotify_url']
    try:
        youtube_link, youtube_music_link, track_info = spotify_to_youtube(spotify_url)
        if youtube_link and youtube_music_link and track_info:
            return jsonify({
                'youtube_link': youtube_link,
                'youtube_music_link': youtube_music_link,
                'artwork_url': track_info['album']['images'][0]['url'] if track_info['album']['images'] else None
            })
        else:
            return jsonify({'error': 'Track not found or not available'}), 404
    except Exception as e:
        print(f"Error in api_spotify_to_youtube: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
