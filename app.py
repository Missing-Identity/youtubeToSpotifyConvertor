from flask import Flask, request, jsonify, render_template
from youtubeToSpotify import youtube_to_spotify, get_youtube_metadata
from spotifyToYoutube import spotify_to_youtube, get_spotify_track_info

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/youtube-to-spotify', methods=['POST'])
def api_youtube_to_spotify():
    youtube_url = request.json['youtube_url']
    spotify_link = youtube_to_spotify(youtube_url)
    if spotify_link:
        title, artist, artwork_url = get_youtube_metadata(youtube_url)
        return jsonify({
            'spotify_link': spotify_link,
            'artwork_url': artwork_url
        })
    else:
        return jsonify({'error': 'Track not found on Spotify'}), 404

@app.route('/api/spotify-to-youtube', methods=['POST'])
def api_spotify_to_youtube():
    spotify_url = request.json['spotify_url']
    youtube_link, youtube_music_link, track_info = spotify_to_youtube(spotify_url)
    if youtube_link and youtube_music_link and track_info:
        return jsonify({
            'youtube_link': youtube_link,
            'youtube_music_link': youtube_music_link,
            'artwork_url': track_info['album']['images'][0]['url'] if track_info['album']['images'] else None
        })
    else:
        return jsonify({'error': 'Track not found or not available'}), 404

if __name__ == '__main__':
    app.run(debug=True)
