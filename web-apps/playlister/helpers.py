from dotenv import load_dotenv
import os, random, string, urllib.parse
from flask import redirect


# Load environment variables
load_dotenv()

# Spotify endpoint & secrets
SPOTIFY_ENDPOINT = 'https://api.spotify.com'
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')


def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


