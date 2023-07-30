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

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/donations', methods=['GET', 'POST'])
def donate():
    return render_template('donations.html')

@app.route('/merch', methods=['GET', 'POST'])
def merch():
    return render_template('merch.html')


@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
    if request.method == 'POST':
        try:
            gc_name = request.form.get('an')
            if not gc_name:
                raise ValueError("Groupchat name not provided in the form.")

            # Create or update the gc node with the 'gc_name' key
            db.child('Groupchats').child(gc_name).set({"groupchat_name": gc_name})

            return redirect(url_for('home', gc_name=gc_name))
        except Exception as e:
            print("Couldn't create group chat")
            print(e)

    groupchats = db.child('Groupchats').get().val()
    groupchats_names = []
    if groupchats:
        groupchats = list(groupchats.values())
        for item in groupchats:
            # Check if 'gc_name' key exists in the item dictionary
            if 'gc_name' in item:
                groupchats_names.append(item['gc_name'])
            else:
                print("Groupchat node doesn't have 'gc_name' key:", item)

    print(groupchats_names)
    return render_template("chatroom.html", groupchats_names=groupchats_names)

@app.route('/ac_chat/<string:gc>', methods=['GET', 'POST'])
def ac_chat(gc):
    if request.method=='POST':
        try:
            me=request.form['message']
            mes={'message':me}
            db.child('Messages').child(gc).push(mes)            
            chat = db.child('Messages').child(gc).get().val()
            return render_template('ac_chat.html', gc=gc, message=me, chat=chat)
        except:
            print("Couldn't find a message ")
    chat = db.child('Messages').child(gc).get().val()
    return render_template('ac_chat.html', gc=gc,chat=chat)


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)