from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
# import sqlite3

app = Flask(__name__)

app.secret_key = '\xbf\xef\xda\xfe\xe8\xd8\x07tW\x97\x05("Gm\xd1$\x9b\xc9\xa4\xe7w\xc7\xf2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

# create the sql alchemy object
db = SQLAlchemy(app)

from models import *

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap

@app.route('/')
@login_required
def home():
	posts = db.session.query(BlogPost).all()
	return render_template('index.html', posts = posts)

@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			session['logged_in'] = True
			flash('You were logged in!')
			return redirect(url_for('home'))
	return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	flash('You were just logged out!')
	return redirect(url_for('welcome'))

# def connect_db():
	# return sqlite3.connect(app.database)

if __name__ == '__main__':
	app.run(debug = True)