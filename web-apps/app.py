from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv


app = Flask(__name__)
# app.app_context().push()

load_dotenv()


@app.route('/')
def home():
    return render_template('index.html')





if __name__ == "__main__":
    app.run()
