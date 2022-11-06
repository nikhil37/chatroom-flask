import os
import random, string
import time as t

from flask import *#Flask,render_template,url_for, session ,redirect , request
from flask_socketio import SocketIO, emit, join_room, leave_room
#from flask_session import Session
from time import localtime,asctime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key='abc'

users=[]
channels={}
pms={}
#Each element should have the following contents
#[timeanddateoftext]=asctime(localtime()).split()
#nameofchannel: {"title":nameofchannel, "timeandtext":[[ [timeanddateoftext] , content of text], ......]}

@app.route("/")
def index():
	if "username" not in session:
		return render_template("login.html")
	elif "last_channel" not in session:
		username=session["username"]
		return render_template("index.html",username=username,channels=list(channels.keys()))
	else:
		x="/"+session["last_channel"]
		return redirect(x)

@app.route('/login',methods=['POST'])
def useradd():
	user=request.form['user']
	if user in users:
		return render_template('login.html',error="Display name already exists")
	session["username"]=user
	users.append(user)
	return redirect('/')

@app.route("/cr/<string:chatroom>")
def chat(chatroom):
	c=channels[chatroom]
	try:
		session["previous_channel"]=session["last_channel"]
	except:
		pass
	session["last_channel"]=chatroom
	return render_template("chatroom.html",chat=c,username=session["username"], channels=list(channels.keys()))

@socketio.on('sent')
def addtext(data):
	sender=session['username']
	timestamp=t.asctime(t.localtime()).split()[3]+" "+t.asctime(t.localtime()).split()[2]+" "+t.asctime(t.localtime()).split()[1]
	message=data['message']
	if(len(message)==0):
		return
	room=data['url'].split('/')[-1]
	#for group channel
	if "/cr/" in data['url']:
		total_messages=len(channels[room]["timeandtext"])
		if total_messages>100:
			channels[room]["timeandtext"].pop(0)
		channels[room]["timeandtext"].append([sender,timestamp,message])
		emit('recieved',{'sender':sender,'time':timestamp,'message':message},room=session["last_channel"])
	else:
		total_messages=len(pms[room]["timeandtext"])
		if total_messages>100:
			pms[room]["timeandtext"].pop(0)
		pms[room]["timeandtext"].append([sender,timestamp,message])
		emit('recieved',{'sender':sender,'time':timestamp,'message':message},room=session["last_channel"])


@socketio.on('nc')
def addnewchanneltolist(data):
	if str(data['rname']) not in list(channels.keys()):
		name=data['rname']
		channels[name]={"title":name,"timeandtext":[]}
		emit('newroom',{'room':name},broadcast=True)
	else:
		return render_template("already_exists.html",username=session["username"],channels=list(channels.keys()))



@socketio.on('change_room_s')
def change_socket_room(u):
	newroom=str(u['url']).split('/')[-1]
	if "previous_channel" in session:
		leave_room(session["previous_channel"])
	join_room(newroom)


@app.route('/check_rooms')
def check():
	return f'''<h1>{len(list(channels.keys()))}</h1><h1>Users:{users}</h1><h1>{list(channels.keys())}</h1>'''


@app.route("/cpm/<string:u2>")
def cpm(u2):
	u1=session["username"]
	if u1<u2:
		x='/pm/'+u1+u2
		return redirect(x)
	elif u2<u1:
		x='/pm/'+u2+u1
		return redirect(x)
	else:
		return redirect("/")

@app.route("/pm/<string:twonames>")
def pm(twonames):
	tw=twonames
	if tw not in list(pms.keys()):
		pms[tw]={"title":tw,"timeandtext":[]}
	c=pms[tw]
	try:
		session["previous_channel"]=session["last_channel"]
	except:
		pass
	session["last_channel"]=tw
	return render_template("chatroom.html",chat=c,username=session["username"], channels=list(channels.keys()))


