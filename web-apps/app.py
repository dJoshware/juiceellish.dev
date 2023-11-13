import os, requests, base64, re

from dotenv import load_dotenv
from playlister.helpers import generate_random_string
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
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
OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
RES_CODE = 'code'
SCOPE = 'user-read-private user-read-email playlist-read-private playlist-modify-private playlist-modify-public ugc-image-upload'
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


# GET ACCESS TOKEN FOR SPOTIFY
@app.route('/playlister/get_spotify_token', methods=['GET', 'POST'])
def get_spotify_token():
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET

    auth_headers = {
        'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode('utf-8')).decode('utf-8')
    }

    auth_data = {
        'grant_type': 'client_credentials',
    }

    auth_url = OAUTH_TOKEN_URL

    res = requests.post(auth_url, headers=auth_headers, data=auth_data)

    if res.status_code == 200:
        body = res.json()
        access_token = body['access_token']
        return access_token
    else:
        return jsonify({'error': 'Failed to get Spotify token'}), res.status_code
    

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

    # Authorize user?
    # get_spotify_token()

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

    # Get user's selected playlist
    _playlist = sp.playlist(id)

    # Playlist name
    name = _playlist['name']
    
    # Playlist description
    description = _playlist['description']

    # Playlist owner
    owner = _playlist['owner']['display_name']
    
    # Flag for playlist cover check
    has_image = True

    # Get playlist info that the user selected
    if name == playlist:
        # If playlist doesn't have cover image, use default
        if _playlist['images']:
            image = _playlist['images'][0]['url']
        else:
            has_image = False
            image = None # Needs value to avoid UnboundLocalError
        
        # Empty list to append song names to
        all_tracks = []
        offset = 0

        # Loop over playlist items to generate list of all the playlist's songs
        while True:
            track_group = sp.playlist_tracks(id, offset=offset)
            tracks = track_group['items']

            if not tracks:
                break # No more tracks to retrieve

            for track in tracks:
                # Extract track name, id, album cover, and artist name and append to empty list
                track_name = track['track']['name']
                track_id = track['track']['id']
                artist_name = track['track']['artists'][0]['name']
                track_album_cover = track['track']['album']['images'][2]['url']

                track_details = {
                    'track_name': track_name,
                    'track_id': track_id,
                    'artist_name': artist_name,
                    'track_album_cover': track_album_cover
                }
                all_tracks.append(track_details)

            # Update offset by 100 for next iteration
            offset += len(tracks)

    return render_template('playlister/playlist.html', name=playlist, id=id, username=username, sm_image=sm_image, image=image, has_image=has_image, description=description, all_tracks=all_tracks, owner=owner)


# Delete playlist
@app.route('/playlister/delete_playlist/<id>')
def delete_playlist(id):
    ''' Delete a playlist from a user's profile. '''

    sp.current_user_unfollow_playlist(playlist_id=id)

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


@app.route('/playlister/edit/<playlist>:<id>', methods=['GET', 'POST'])
def edit_playlist(playlist, id):
    ''' Allow user to edit selected playlist. '''

    # Get user profile information to display username
    user = sp.current_user()
    username = user['display_name']
    sm_image = user['images'][0]['url']

    # Get user's selected playlist
    _playlist = sp.playlist(id)

    # Playlist name
    name = _playlist['name']
    
    # Playlist description
    description = _playlist['description']

    # Playlist owner
    owner = _playlist['owner']['display_name']

    # Flag for playlist cover check
    has_image = True

    # Get playlist info that the user selected
    if name == playlist:
        # If playlist doesn't have cover image, use default
        if not _playlist['images']:
            has_image = False
            image = None # Needs value to avoid UnboundLocalError
        else:
            image = _playlist['images'][0]['url']

        # Empty list to append track uris to
        all_tracks = []
        offset = 0

        # Loop over playlist items to generate list of all the playlist's songs
        while True:
            track_group = sp.playlist_tracks(id, offset=offset)
            tracks = track_group['items']

            if not tracks:
                break # No more tracks to retrieve

            for track in tracks:
                # Extract track name, id, album cover, and artist name and append to empty list
                track_name = track['track']['name']
                track_id = track['track']['id']
                artist_name = track['track']['artists'][0]['name']
                track_album_cover = track['track']['album']['images'][2]['url']

                track_details = {
                    'track_name': track_name,
                    'track_id': track_id,
                    'artist_name': artist_name,
                    'track_album_cover': track_album_cover
                }
                all_tracks.append(track_details)

            # Update offset by 100 for next iteration
            offset += len(tracks)

    # Save changes made when editing playlist
    if request.method == 'POST':

        # image_edit = request.form.get('cover_image')
        # if image_edit:
            
        #     sp.playlist_upload_cover_image(playlist_id=id, image_b64=image_edit)
        
        title_edit = request.form.get('playlist_name')
        description_edit = request.form.get('playlist_desc')
        selectedIds = request.form.get('selectedIds')
        
        sp.playlist_change_details(playlist_id=id, name=title_edit, description=description_edit)

        if not selectedIds == '':
            all_tracks_edit = selectedIds.split(',')
            sp.playlist_remove_all_occurrences_of_items(playlist_id=id, items=all_tracks_edit)
        else:
            pass
        
        return redirect('/playlister/index')


    return render_template('playlister/edit_playlist.html', name=playlist, id=id, username=username, sm_image=sm_image, image=image, has_image=has_image, description=description, all_tracks=all_tracks, owner=owner)


if __name__ == "__main__":
    app.run()
