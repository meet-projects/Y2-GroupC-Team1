from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyDeCR2mPfW9yT__WZ0F90IEhSwjYU4TOi8",
  "authDomain": "y2-groupc-team1.firebaseapp.com",
  "projectId": "y2-groupc-team1",
  "storageBucket": "y2-groupc-team1.appspot.com",
  "messagingSenderId": "289049142886",
  "appId": "1:289049142886:web:aa1fb5cf71fad3cb392fa7",
  "databaseURL" : "https://y2-groupc-team1-default-rtdb.firebaseio.com/"
}


@app.route('/donations', methods=['GET', 'POST'])
def donate():
    return render_template('donations.html')


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)