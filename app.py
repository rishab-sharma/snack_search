from flask import Flask, render_template, request , session
import sqlite3
import flask , os
import pandas as pd
from sklearn.externals import joblib
import datetime
import numpy as np

# Neural Network Load

from keras.models import model_from_json
json_file = open('models/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("models/model.h5")
print("Loaded model from disk")


datetime.datetime.today()
date = datetime.datetime.today().weekday()
if date == 0:
	day = "Monday"
elif date == 1:
	day = "Tuesday"
elif date == 2:
	day = "Wednesday"
elif date == 3:
	day = "Thursday"
elif date == 4:
	day = "Friday"
elif date == 5:
	day = "Saturday"
elif date == 6:
	day = "Sunday"

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

@app.route('/recommend')
def recommend():
	if 'user' in session:
		return render_template('recommend.html')
	else:
		return "<h1 style='text-align:center'>Sorry Your Session has expired !</h1>"

@app.route('/load_model',methods=['GET','POST'])
def load_model():
	if 'user' in session:
		count = 0
		count += 1
		import random
		random.Random(count)
		req = request.get_json()
		algo = str(req['algo'])
		if algo == "SVM":
			clf = joblib.load('models/svc_40.pkl') 
			email = session['user']
			print email
			habit = pd.read_sql("""SELECT h_{} FROM habits WHERE email = {} """.format(date+1 , email), connection).values[0][0]
			print habit
			habit2 = '"' + str(habit) + '"'
			(p,f,c,s) = pd.read_sql("""SELECT protein , fat , calories , sodium FROM recepies WHERE title = {}""".format(habit2), connection).values[0]
			print p,f,c,s
			output = clf.predict([[p,f,c,s]])
			print output
			prediction = pd.read_sql("""SELECT title FROM recepies WHERE types = {} """.format(output[0]), connection).values[0]
			op = random.choice (prediction)
			op2 = '"' + str(op) + '"'
			(p,f,c,s) = pd.read_sql("""SELECT protein , fat , calories , sodium FROM recepies WHERE title = {}""".format(op2), connection).values[0]
			d = {
			'snack': op,
			'habit': habit,
			'day': day,
			'protein':p,
			'fat':f,
			'calories':c,
			'sodium':s
			}
			res = flask.jsonify(d)
			return res

		elif algo == "RF":
			clf = joblib.load('models/rf_40.pkl') 
			email = session['user']
			print email
			habit = pd.read_sql("""SELECT h_{} FROM habits WHERE email = {} """.format(date+1 , email), connection).values[0][0]
			print habit
			habit2 = '"' + str(habit) + '"'
			(p,f,c,s) = pd.read_sql("""SELECT protein , fat , calories , sodium FROM recepies WHERE title = {}""".format(habit2), connection).values[0]
			print p,f,c,s
			output = clf.predict([[p,f,c,s]])
			print output
			prediction = pd.read_sql("""SELECT title FROM recepies WHERE types = {} """.format(output[0]), connection).values[0]
			op = random.choice (prediction)
			op2 = '"' + str(op) + '"'
			(p,f,c,s) = pd.read_sql("""SELECT protein , fat , calories , sodium FROM recepies WHERE title = {}""".format(op2), connection).values[0]
			d = {
			'snack': op,
			'habit': habit,
			'day': day,
			'protein':p,
			'fat':f,
			'calories':c,
			'sodium':s
			}
			res = flask.jsonify(d)
			return res
		elif algo == "DT":
			clf = joblib.load('models/dt_40.pkl') 
			email = session['user']
			print email
			habit = pd.read_sql("""SELECT h_{} FROM habits WHERE email = {} """.format(date+1 , email), connection).values[0][0]
			print habit
			habit2 = '"' + str(habit) + '"'
			(p,f,c,s) = pd.read_sql("""SELECT protein , fat , calories , sodium FROM recepies WHERE title = {}""".format(habit2), connection).values[0]
			print p,f,c,s
			output = clf.predict([[p,f,c,s]])
			print output
			prediction = pd.read_sql("""SELECT title FROM recepies WHERE types = {} """.format(output[0]), connection).values[0]
			op = random.choice (prediction)
			op2 = '"' + str(op) + '"'
			(p,f,c,s) = pd.read_sql("""SELECT protein , fat , calories , sodium FROM recepies WHERE title = {}""".format(op2), connection).values[0]
			d = {
			'snack': op,
			'habit': habit,
			'day': day,
			'protein':p,
			'fat':f,
			'calories':c,
			'sodium':s
			}
			res = flask.jsonify(d)
			return res
		elif algo == "NN": 
			email = session['user']
			print email
			habit = pd.read_sql("""SELECT h_{} FROM habits WHERE email = {} """.format(date+1 , email), connection).values[0][0]
			print habit
			habit2 = '"' + str(habit) + '"'
			(p,f,c,s) = pd.read_sql("""SELECT protein , fat , calories , sodium FROM recepies WHERE title = {}""".format(habit2), connection).values[0]
			print p,f,c,s
			X = np.array([p,f,c,s])
			output = loaded_model.predict_classes(X.reshape(1,4), verbose=0)
			print output
			prediction = pd.read_sql("""SELECT title FROM recepies WHERE types = {} """.format(output[0]), connection).values[0]
			op = random.choice (prediction)
			op2 = '"' + str(op) + '"'
			(p,f,c,s) = pd.read_sql("""SELECT protein , fat , calories , sodium FROM recepies WHERE title = {}""".format(op2), connection).values[0]
			d = {
			'snack': op,
			'habit': habit,
			'day': day,
			'protein':p,
			'fat':f,
			'calories':c,
			'sodium':s
			}
			res = flask.jsonify(d)
			return res
	else:
		return "<h1 style='text-align:center'>Sorry Your Session has expired !</h1>"

@app.route('/habits',methods=['GET','POST'])
def habits():
	if 'user' in session:
		req = request.get_json()
		h_1 = str(req['monday'])
		h_2 = str(req['tuesday'])
		h_3 = str(req['wednesday'])
		h_4 = str(req['thursday'])
		h_5 = str(req['friday'])
		h_6 = str(req['saturday'])
		h_7 = str(req['sunday']) 
		print h_1 , h_2 , h_3 , h_3 , h_4 , h_5 , h_6 , h_7
		email = session['user']  
		user_id = pd.read_sql("""SELECT user_id FROM users WHERE email = {}""".format(email), connection).values[0][0]
		sql = """INSERT INTO habits( user_id , email , h_1 , h_2 , h_3 , h_4 , h_5 , h_6 , h_7 ) VALUES ( ? , ? , ? , ? , ? , ? , ? , ? , ?);"""
		c.execute(sql , ( user_id , email , h_1 , h_2 , h_3 , h_4 , h_5 , h_6 , h_7 ))
		connection.commit()
		res = {"status": True}
		res = flask.jsonify(res)
		return res
	else:
		return "<h1 style='text-align:center'>Sorry Your Session has expired !</h1>"
connection.commit()
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0' , port = port)






