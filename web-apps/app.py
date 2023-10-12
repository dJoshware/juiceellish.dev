import os, requests

from dotenv import load_dotenv
from playlister.helpers import generate_random_string
from flask import Flask, render_template, request, redirect, url_for, session
from flask_caching import Cache
from flask_session import Session
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import urllib.parse


# Load environment variables
load_dotenv()

# Configure simple caching
config = {
    'DEBUG': True,
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300
}

# Application configurations
app = Flask(__name__)
app.config.from_mapping(config)
app.secret_key = os.getenv('SECRET_KEY')
cache = Cache(app)
# Session(app)

# Constants
OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize?'
# OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
RES_CODE = 'code'
SCOPE = 'user-read-private user-read-email playlist-read-private playlist-modify-private playlist-modify-public'
STATE = generate_random_string(16)

params = {
            'response_type': RES_CODE,
            'client_id': CLIENT_ID,
            'scope': SCOPE,
            'redirect_uri': REDIRECT_URI,
            'state': STATE,
            'show_dialog': True
        }

oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    state=STATE,
    scope=SCOPE,
    show_dialog=True
)

sp = Spotify(auth_manager=oauth)


# PORTFOLIO ROUTES

# Home route / juiceellish.dev landing page
@app.route('/')
def home():
    ''' Landing page for 'juiceellish.dev'. '''
    
    # Setup as portfolio
    # Describe backend of the site, showcase applications at top (as cards: image, title, and description), explain languages used and any respective packages/modules, hosting service(s)
    # Create backstory/personal background section

    return render_template('index.html')


# ----- PLAYLISTER ROUTES -----

# Landing page
@app.route('/playlister/index')
# @cache.cached()
def playlister_index():
    ''' Playlister app landing page. '''

    # Get user profile information to display username
    user = sp.current_user()

    # Username
    username = user['display_name']

    # PFPs
    sm_image = user['images'][0]['url']
    # lg_image = user['images'][1]['url']

    # Get user playlists
    playlists = sp.current_user_playlists()

    return render_template('playlister/index.html', playlists=playlists, username=username, sm_image=sm_image)

# Playlists page
@app.route('/playlister/<playlist>:<id>')
def playlister_playlist(playlist, id):
    ''' Takes a playlist the user selects and renders it on its own page. '''

    # Get user profile information to display username
    user = sp.current_user()
    username = user['display_name']
    sm_image = user['images'][0]['url']

    # Get user playlists
    playlists = sp.current_user_playlists()

    # Flag for playlist cover check
    has_image = True

    # Loop over playlists to get cover image, name, description, and id
    for item in playlists['items']:
        # Get playlist info that the user selected
        if item['name'] == playlist:
            # If playlist doesn't have cover image, use default
            if not item['images']:
                has_image = False
                image = None # Needs value to avoid UnboundLocalError
            else:
                image = item['images'][0]['url']
            
            description = item['description']

            # Empty list to append song names to
            all_track_names = []
            offset = 0

            # Loop over playlist items to generate list of all the playlist's songs
            while True:
                track_group = sp.playlist_tracks(id, offset=offset)
                tracks = track_group['items']

                if not tracks:
                    break # No more tracks to retrieve

                for track in tracks:
                    # Extract track name and append to empty list
                    track_name = track['track']['name']
                    all_track_names.append(track_name)

                # Update offset by 100 for next iteration
                offset += len(tracks)

            # ARTIST NAME
            # print(track['track']['album']['artists'][0]['name'])

            # ALBUM NAME OF TRACK
            # print(track['track']['album']['name'])

            # ALBUM IMAGES
            # print(track['track']['album']['images'][0]['url'])
            # print(track['track']['album']['images'][1]['url'])
            # print(track['track']['album']['images'][2]['url'])

            # TRACK NAME
            # tracks = track['track']['name']


    return render_template('playlister/playlist.html', name=playlist, id=id, username=username, sm_image=sm_image, image=image, has_image=has_image, description=description, all_track_names=all_track_names)

# Delete playlist
@app.route('/playlister/delete_playlist/<id>')
def delete_playlist(id):
    ''' Delete a playlist from a user's profile. '''

    # Test functionality
    playlist = sp.playlist(id)
    for item in playlist['tracks']['items']:
        print(item)
    '''
    FIX:
        PRINT ALL PLAYLIST ITEMS; CUTS OFF AT 100
        GET LIST OF TRACK URIS
        EXAMPLE:
        {
            "tracks": [
                {
                    "uri": "spotify:track:4iV5W9uYEdYUVa79Axb7Rh"
                },
                {
                    "uri": "spotify:track:1301WleyT98MSxVHPZCA6M"
                }
            ]
        }
    '''
    # print(playlist['tracks']['items'][1])

    # sp.playlist_remove_all_occurrences_of_items(playlist_id=id)
    print(f'Playlist {id} DELETED')

    return redirect('/playlister/index')


# Create playlist
@app.route('/playlister/create_playlist', methods=['GET', 'POST'])
def create_playlist():
    ''' Create new playlist to save to user profile. '''

    # Get user profile information to display username
    user = sp.current_user()
    username = user['display_name']
    sm_image = user['images'][0]['url']

    # Spotipy parameters for creating playlists
    public_param = True
    collab_param = False

    if request.method == 'POST':
        playlist_name = request.form.get('playlist_name')
        description = request.form.get('playlist_desc')
        # pfp = request.form.get('playlist_img')
        public = request.form.get('public')
        collaborative = request.form.get('collaborative')

        # Check if user unselected Public
        if public == None:
            public_param = False
        # Check if user selected Collaborative
        if collaborative == 'on':
            collab_param = True

        sp.user_playlist_create(user=user['id'], name=playlist_name, public=public_param, collaborative=collab_param, description=description)

        return redirect('/playlister/index')

    return render_template('playlister/create_playlist.html', username=username, sm_image=sm_image)


if __name__ == "__main__":
    app.run()
