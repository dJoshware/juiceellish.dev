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
OAUTH_AUTHORIZE_URL= 'https://accounts.spotify.com/authorize?'
OAUTH_TOKEN_URL= 'https://accounts.spotify.com/api/token'
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




# Home route / juiceellish.dev landing page
@app.route('/')
def home():
    ''' Landing page for 'juiceellish.dev'. '''
    # Setup as portfolio
    # Describe backend of the site, showcase applications at top (as cards: image, title, and description), explain languages used and any respective packages/modules, hosting service(s)
    # Create backstory/personal background section

    return render_template('index.html')


# ----- PLAYLISTER ROUTES -----

# Login page
@app.route('/playlister/login', methods=['GET', 'POST'])
def login():
    ''' Log user in. '''
    if request.method == 'POST':
        params['show_dialog'] # Working on login functionality
        encoded_params = urllib.parse.urlencode(params)

        return redirect(OAUTH_AUTHORIZE_URL + encoded_params)
    return render_template('playlister/login.html')


# Logout functionality; redirect to login page
@app.route('/playlister/logout', methods=['GET', 'POST'])
def logout():
    ''' Log user out. '''
    params['show_dialog'] = False
    encoded_params = urllib.parse.urlencode(params)
    response = requests.get(OAUTH_AUTHORIZE_URL + encoded_params)
    if request.method == 'POST':
        # "Log In" button - id='login-button'
        return 
    # return redirect('/playlister/login')
    return response.text


# Landing page
@app.route('/playlister/index')
@cache.cached()
def playlister_index():
    ''' Playlister app landing page. '''
    # Get user profile information to display username
    user = sp.current_user()
    print(user)

    # Username
    username = user['display_name']

    # PFPs
    sm_image = user['images'][0]['url']
    lg_image = user['images'][1]['url']

    # Get user playlists
    playlists = sp.current_user_playlists()
        # style them in card form, 250px by 250px; stack vertically, title, description, edit & delete buttons
    
    # Create 'Edit Playlist', 'Delete Playlist' and 'Create New Playlist' buttons on the form page
    # Username and PFP top right page, logout button
        # Logout: logout of Spotify and 

    return render_template('playlister/index.html', playlists=playlists, username=username, sm_image=sm_image, lg_image=lg_image)

# Playlists page
@app.route('/playlister/<playlist>')
def playlister_playlist(playlist):
    ''' Takes a playlist the user selects and renders it on its own page. '''
    # Get user profile information to display username
    user = sp.current_user()
    username = user['display_name']

    # Get user playlists
    playlists = sp.current_user_playlists()

    # Loop over playlists to get cover image, name, description, and id
    for item in playlists['items']:
        # Get playlist info that the user selected
        if item['name'] == playlist:
            image = item['images'][0]['url']
            description = item['description']
            id = item['id']

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
        
            # print(f'Track total: {len(all_track_names)}')
            # if len(all_track_names) > 0:
            #     print(all_track_names)

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


    return render_template('playlister/playlist.html', name=playlist, username=username, image=image, description=description, all_track_names=all_track_names)



if __name__ == "__main__":
    app.run()
