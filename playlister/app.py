from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)
# app.app_context().push()


@app.route('/')
def home():
    return render_template('index.html')





if __name__ == "__main__":
    app.run()