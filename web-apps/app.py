import os, requests, base64 #, json

from datetime import datetime as dt
from dotenv import load_dotenv
from playlister.helpers import generate_random_string
from flask import Flask, flash, jsonify, render_template, request, redirect, session
# from flask_caching import Cache
from flask_session import Session
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler


# Load environment variables
load_dotenv()

# Configure simple caching
# config = {
#     'DEBUG': True,
#     'CACHE_TYPE': 'SimpleCache',
#     'CACHE_DEFAULT_TIMEOUT': 300
# }

# Application configurations
app = Flask(__name__)
# app.config.from_mapping(config)
app.secret_key = os.getenv('SECRET_KEY')
# cache = Cache(app)
Session(app)

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

# oauth = SpotifyOAuth(
#     client_id=CLIENT_ID,
#     client_secret=CLIENT_SECRET,
#     redirect_uri=REDIRECT_URI,
#     state=STATE,
#     scope=SCOPE,
#     show_dialog=True
# )

# sp = Spotify(auth_manager=oauth)


# GET ACCESS TOKEN FOR SPOTIFY
@app.route('/playlister/get_spotify_token', methods=['GET', 'POST'])
def get_spotify_token():
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET

    auth_url = OAUTH_TOKEN_URL

    auth_headers = {
        'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode('utf-8')).decode('utf-8')
    }

    auth_data = {
        'grant_type': 'client_credentials',
    }

    res = requests.post(auth_url, headers=auth_headers, data=auth_data)

    if res.status_code == 200:
        body = res.json()
        access_token = body['access_token']
        return redirect('/playlister/index')
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
def playlister_index():
    ''' Playlister app landing page. '''

    cache_handler = FlaskSessionCacheHandler(session)
    auth_manager = SpotifyOAuth(
        scope = SCOPE,
        cache_handler=cache_handler,
        redirect_uri=REDIRECT_URI,
        show_dialog = True
    )

    if request.args.get('code'):
        print('Step 2 triggered')
        # Step 2. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get('code'))
        return redirect('/playlister/index')
    
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        print('Step 1 triggered')
        # Step 1. Display sign in link if no token
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'
    
    # Step 3. Signed in, display data
    sp = Spotify(auth_manager=auth_manager)
    print('Step 3 triggered')

    # Get user profile information to display username
    user = sp.current_user()

    # Username
    username = user['display_name']

    # PFPs
    sm_image = user['images'][0]['url']
    # lg_image = user['images'][1]['url']

    # Get user playlists
    playlists = sp.current_user_playlists() # limit 50...
    #NOTE CREATE LOOP TO GET THROUGH ALL PLAYLISTS IF OVER 50

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
    public_param = False
    collab_param = False

    if request.method == 'POST':
        playlist_name = request.form.get('playlist_name')
        description = request.form.get('playlist_desc')
        # pfp = request.form.get('playlist_img')
        public = request.form.get('public')
        collaborative = request.form.get('collaborative')

        # Check if user selected Public
        if public == 'on':
            public_param = True
        # Check if user selected Collaborative
        if collaborative == 'on':
            collab_param = True

        if public == 'on' and collaborative == 'on':
            flash('Collaborative playlists can only be private!')
            return redirect('/playlister/create_playlist')

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
        if _playlist['images']:
            image = _playlist['images'][0]['url']
        else:
            has_image = False
            image = None # Needs value to avoid UnboundLocalError

        # Empty list to append track uris to
        all_tracks = []
        offset = 0

        # Loop over playlist items to generate list of all the playlist's songs
        while True:
            track_group = sp.playlist_tracks(id, offset=offset)
            tracks = track_group['items']

            if not tracks:
                break

            for track in tracks:
                # Extract track name, id, album cover, and artist name and append to empty list
                track_details = {
                    'track_name': track['track']['name'],
                    'track_id': track['track']['id'],
                    'artist_name': track['track']['artists'][0]['name'],
                    'track_album_cover': track['track']['album']['images'][2]['url']
                }
                all_tracks.append(track_details)

            # Update offset by 100 for next iteration
            offset += len(tracks)

    # Save changes made when editing playlist
    if request.method == 'POST':

        # CUSTOM IMAGE UPLOAD NEEDS WORK
        # image_edit = request.form.get('cover_image')
        # if image_edit:
            
        #     sp.playlist_upload_cover_image(playlist_id=id, image_b64=image_edit)
        
        title_edit = request.form.get('playlist_name')
        description_edit = request.form.get('playlist_desc')
        selectedIds = request.form.get('selectedIds')

        if title_edit and description_edit:
            sp.playlist_change_details(playlist_id=id, name=title_edit, description=description_edit)

        if not selectedIds == '':
            all_tracks_edit = selectedIds.split(',')
            sp.playlist_remove_all_occurrences_of_items(playlist_id=id, items=all_tracks_edit)
        else:
            pass
        
        return redirect('/playlister/index')


    return render_template('playlister/edit_playlist.html', name=playlist, id=id, username=username, sm_image=sm_image, image=image, has_image=has_image, description=description, all_tracks=all_tracks, owner=owner)


@app.route('/playlister/search:<id>', methods=['GET', 'POST'])
def playlister_search(id):
    ''' Let user search for artists, albums, songs, episodes, or playlists and add them to their library. '''

    # Call in template to get songs for each album
    def get_album(id):
        ''' Return songs of an album. '''

        album = sp.album(album_id=id)
        items = album['tracks']['items']
        all_songs = []
        for song in items:
            song = {
                'song_image': album['images'][2]['url'],
                'song_name': song['name'],
                'song_id': song['id']
            }
            all_songs.append(song)
        return all_songs

    # Get id for flask error messaging redirection
    playlist_id = id

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

    # If playlist doesn't have cover image, use default
    if not _playlist['images']:
        has_image = False
        image = None # Needs value to avoid UnboundLocalError
    else:
        image = _playlist['images'][0]['url']
    
    # Empty list to send to template
    sorted_albums = []

    if request.method == 'POST':
        # Takes search query from user in search bar
        query = request.form.get('search_bar').strip()
        # If user typed anything, continues
        if query:
            # Searches the query using spotipy and returns a list of artists
            search = sp.search(q=query, type='artist')
            # Gets artists name and Spotify id from search result
            artist_name = search['artists']['items'][0]['name'].lower()
            artist_id = search['artists']['items'][0]['id']
            # If the search result name and user query match, continues
            if artist_name == query.lower():
                # Empty list to append album details to
                offset = 0
                all_artist_albums = []
                # Loop over details of artist albums to generate new list to use in search.html
                while True:
                    # Using user's query, return a list of the artist's albums
                    artist_albums = sp.search(q=query, type='album', offset=offset)
                    albums = artist_albums['albums']['items']
                    
                    if not albums:
                        break # If nothing returned

                    # Loop through each item returned in 'albums'
                    for album in albums:
                        # If the artist's id from the first artist search query matches the artist's id found in the album search query, continue
                        if artist_id == album['artists'][0]['id']:
                            # Create custom dictionary to use in search.html
                            album_details = {
                                'release_date': album['release_date'],
                                'artist_name': album['artists'][0]['name'],
                                'album_name': album['name'],
                                'album_id': album['id'],
                                'album_cover_image': album['images'][2]['url'],
                                'album_type': album['album_type'],
                                'total_tracks': album['total_tracks']
                            }
                            # Append to empty list
                            all_artist_albums.append(album_details)
                    # Increase offset of spotipy's 'search' function to iterate over all of artist's albums
                    offset += len(albums)
                    if offset == 1000: # app breaks without this
                        break
                # Create new empty dictionary for sorted albums
                album_dict = {}
                # Loop over first empty list after it's filled
                for album in all_artist_albums:
                    release_date = album['release_date']
                    album_name = album['album_name']
                    album_type = album['album_type']

                    # Check if release_date is already in YYYY format
                    if len(release_date) == 4:
                        formatted_release_date = release_date
                    else:
                        formatted_release_date = dt.strptime(release_date, '%Y-%m-%d').strftime('%Y')

                    # Check if album_name is already in dictionary
                    if album_name in album_dict:
                        # Check album_type and compare release_dates to find most recent one
                        if album_type == 'single' or (album_type == 'album' and formatted_release_date > album_dict[album_name]['release_date']):
                            album_dict[album_name] = {'release_date': formatted_release_date, **album}
                    else:
                        # If album_name not in dictionary, add it
                        album_dict[album_name] = {'release_date': formatted_release_date, **album}
                
                # Sort album_dict by release_date in descending order
                sorted_albums = sorted(album_dict.values(), key=lambda x: (x['album_type'] == 'album', x['release_date'], x['album_name'], x['album_id'], x['total_tracks']), reverse=True)
            else:
                # If artist search query is incomplete
                flash("ERROR: Unfinished query")
                flash("Please provide an artist's full name.")
                return redirect(f'/playlister/search:{playlist_id}')
        else:
            # If user doesn't type anything
            flash("ERROR: No input")
            flash("Please provide an artist's full name.")
            return redirect(f'/playlister/search:{playlist_id}')


    return render_template('playlister/search.html', name=name, id=id, username=username, sm_image=sm_image, image=image, has_image=has_image, description=description, owner=owner, sorted_albums=sorted_albums, get_album=get_album)


@app.route('/playlister/add_to_playlist/<playlist>:<id>')
def add_to_playlist(playlist, id):
    ''' Add an item to a playlist. '''

    track = [id]
    sp.playlist_add_items(playlist_id=playlist, items=track)

    return ''


if __name__ == "__main__":
    app.run()
