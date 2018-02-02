from flask import Flask, render_template, request , session
import sqlite3
import flask , os
import pandas as pd

app = Flask(__name__)

app.secret_key = os.urandom(24)

database = 'snack_search'

connection = sqlite3.connect('database/{}.db'.format(database))

c = connection.cursor()

def create_user_table():
	sql = "CREATE TABLE IF NOT EXISTS users( user_id INTEGER PRIMARY KEY AUTOINCREMENT , u_name TEXT , email TEXT , pass TEXT );"
	c.execute(sql)

def session_manager():
	sql = "CREATE TABLE IF NOT EXISTS session( session_id INTEGER PRIMARY KEY AUTOINCREMENT , user_id INTEGER , u_name TEXT , session_token TEXT );"
	c.execute(sql)

def habits():
	sql = "CREATE TABLE IF NOT EXISTS habits( habit_id INTEGER PRIMARY KEY AUTOINCREMENT , user_id INTEGER , u_name TEXT , h_1 TEXT , h_2 TEXT , h_3 TEXT , h_4 TEXT , h_5 TEXT , h_6 TEXT , h_7 TEXT);"
	c.execute(sql)

@app.route('/create-db')
def db():
	create_user_table()
	session_manager()
	habits()
	return "Done...Database Created"

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/detail')
def detail():
	if 'user' in session:
		return render_template('detail.html')
	else:
		return "<h1 style='text-align:center'>Sorry Your Session has expired !</h1>"


@app.route('/register',methods=['GET','POST'])
def register():
	req = request.get_json()
	email = str(req['email']) 
	password = str(req['password'])
	u_name = str(req['u_name'])
	print email , password , u_name
	sql = """INSERT INTO users( u_name , email , pass ) VALUES ( ? , ? , ?);"""
	c.execute(sql , ( u_name , email , password))
	connection.commit()
	res = {"status": True}
	res = flask.jsonify(res)
	session['user'] = email
	return res

@app.route('/login',methods=['GET','POST'])
def login():
	req = request.get_json()
	email = '"' + str(req['email']) + '"' 
	password = '"' + str(req['password']) + '"'
	user = pd.read_sql("""SELECT * FROM users WHERE email = {} and pass = {}""".format(email , password), connection).values[0]
	connection.commit()
	res = {"status": True}
	res = flask.jsonify(res)
	session['user'] = email
	return res

@app.route('/logout')
def logout():
	session.pop('user',None)
	return render_template('index.html')

connection.commit()
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0' , port = port)






