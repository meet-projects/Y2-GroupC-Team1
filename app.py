from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(_name_, template_folder='templates', static_folder='static')
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
    return render_template('home.html')

@app.route('/donations', methods=['GET', 'POST'])
def donate():
    error=""
    if request.method == 'POST':
        name= request.form["donor-name"]
        email= request.form["email"]
        currency= request.form["currency"]
        amount = request.form["amount"]
        types = request.form["donation-type"]
        try:
            donation={"amount":amount,"name":name, "currency":currency, "email":currency,"types":types}
            db.child('Donations').push(donation)
            return redirect(url_for('chatroom'))
        except Exception as e:
            print("error")
            print(e)

    return render_template('donations.html')



@app.route('/merch', methods=['GET', 'POST'])
def merch():
    return render_template('merch.html')

@app.route ('/news&events', methods=['GET', 'POST'])
def news_events():
    return render_template('news_events.html')

@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
    if request.method == 'POST':
        try:
            groupchat_name = request.form.get('an')
            if not groupchat_name:
                raise ValueError("Groupchat name not provided in the form.")
            # Create or update the groupchat node with the 'groupchat_name' key
            db.child('Groupchats').child(groupchat_name).set({"groupchat_name": groupchat_name})
            return redirect(url_for('ac_chat', groupchat=groupchat_name))
        except Exception as e:
            print("Couldn't create group chat")
            print(e)

    groupchats = db.child('Groupchats').get().val()
    groupchats_names = []
    if groupchats:
        groupchats = list(groupchats.values())
        for item in groupchats:
            # Check if 'groupchat_name' key exists in the item dictionary
            if 'groupchat_name' in item:
                groupchats_names.append(item['groupchat_name'])
            else:
                print("Groupchat node doesn't have 'groupchat_name' key:", item)

    print(groupchats_names)
    return render_template("chatroom.html", groupchats_names=groupchats_names)


# @app.route('/news_letter', methods=['GET', 'POST'])
# def news_letter():
#   error = ""
#   if request.method == 'POST':
#       uname = request.form['name']
#       uemail = request.form['email']
#       try:
#           signed_user = {'name' : uname, 'email' : uemail}
#           db.child('Newsletter-Users').push(signed_user)
#           return redirect('home')
#       except Exception as e:
#           print("Couldn't signup to the news letter")
#           print(e)
#   return render_template('news-letter.html')


@app.route('/ac_chat/<string:groupchat>', methods=['GET', 'POST'])
def ac_chat(groupchat):
    if request.method=='POST':
        try:
            me=request.form['message']
            mes={'message':me}
            db.child('Messages').child(groupchat).push(mes)
            chat = db.child('Messages').child(groupchat).get().val()
            return render_template('ac_chat.html', groupchat=groupchat, message=me, chat=chat)
        except:
            print("Couldn't find a message")
    chat = db.child('Messages').child(groupchat).get().val()
    return render_template('ac_chat.html', groupchat=groupchat, chat=chat)


# @app.route('/donations-second', methods=['GET', 'POST'])
# def emaillist():
#   error=""
#   if request.method=='POST':
#       email= request.form['email2']
#       fullname= request.form['fullname2']
#       try:
#           subscription = {'fullname' : fullname, 'email' : email}
#           db.child('suscribers').push(subscription)
#           return redirect(url_for('donate'))
#       except:
#           error="error"
#   return redirect(url_for('donate'))



if _name_ == '_main_':
    app.run(debug=True)