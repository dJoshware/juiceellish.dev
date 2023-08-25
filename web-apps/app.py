from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from flask_caching import Cache

load_dotenv()

config = {
    'DEBUG': True,
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/playlister_index')
def playlister_index():
    return render_template('playlister/index.html')


if __name__ == "__main__":
    app.run()
