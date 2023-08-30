import os
from dotenv import load_dotenv
from playlister.helpers import login
from flask import Flask, render_template, request, redirect, url_for, session
from flask_caching import Cache

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


# Home route / juiceellish.dev landing page
@app.route('/')
def home():

    # Setup as portfolio
    # Describe backend of the site, showcase applications at top (as cards: image, title, and description), explain languages used and any respective packages/modules, hosting service(s)
    # Create backstory/personal background section

    return render_template('index.html')


# Playlister app landing page
@app.route('/playlister_index', methods=['GET', 'POST'])
@cache.cached(timeout=60)
def playlister_index():

    # If user submits Spotify login form
        # Log user in to their Spotify account
    # Get all existing playlists: style them in card form
    # Create 'Edit Playlist', 'Delete Playlist' and 'Create New Playlist' buttons on the form page


    return render_template('playlister/index.html')


if __name__ == "__main__":
    app.run()
