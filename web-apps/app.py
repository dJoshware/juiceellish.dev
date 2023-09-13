import os, requests

from dotenv import load_dotenv
from playlister.helpers import generate_random_string
from flask import Flask, render_template, request, redirect, url_for, session
from flask_caching import Cache
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


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

OAUTH_AUTHORIZE_URL= 'https://accounts.spotify.com/authorize'
OAUTH_TOKEN_URL= 'https://accounts.spotify.com/api/token'


oauth = SpotifyOAuth(client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                     client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),redirect_uri=os.getenv('REDIRECT_URI'), state=generate_random_string(16), scope="user-read-private user-read-email playlist-read-private playlist-modify-private playlist-modify-public")

sp = Spotify(auth_manager=oauth)




# Home route / juiceellish.dev landing page
@app.route('/')
def home():

    # Setup as portfolio
    # Describe backend of the site, showcase applications at top (as cards: image, title, and description), explain languages used and any respective packages/modules, hosting service(s)
    # Create backstory/personal background section

    return render_template('index.html')


# Playlister app landing page
@app.route('/playlister/index')
@cache.cached(timeout=60)
def playlister_index():
    playlist = sp.current_user_playlists(limit=5)
    user = sp.current_user()
    
    print(playlist)

    # Get all existing playlists: style them in card form, 250px by 250px; stack vertically, title, description, edit & delete buttons
    # Create 'Edit Playlist', 'Delete Playlist' and 'Create New Playlist' buttons on the form page
    # Username and PFP top right page, logout button
        # Logout: logout of Spotify and 

    return render_template('playlister/index.html', playlist=playlist, user=user)


if __name__ == "__main__":
    app.run()
