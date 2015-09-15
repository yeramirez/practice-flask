from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from python_mysql_connect2 import connect
import hashlib
from form import LoginForm
from python_mysql_dbselect import select_user
from python_mysql_dbinsert import insert_user
from werkzeug.security import generate_password_hash, \
     check_password_hash

app = Flask(__name__)

app.secret_key = '\xbf\xef\xda\xfe\xe8\xd8\x07tW\x97\x05("Gm\xd1$\x9b\xc9\xa4\xe7w\xc7\xf2'


# -------     Login Required     ------- #
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap



# -------     Index     ------- #
@app.route('/')
@login_required
def home():
	return render_template('index.html')



# -------     Welcome     ------- #
@app.route('/welcome')
def welcome():
	return render_template('welcome.html')



# -------     Registration Class     ------- #

@app.route('/register', methods=['GET', 'POST'])
def register():

	if request.method == 'POST':
		uname = request.form['username']
		pword = generate_password_hash(request.form['password'])
		emall = request.form['email']

		insert_user(uname, pword, emall)
		flash('Thanks for registering')
		return redirect(url_for('welcome'))
	return render_template('register.html')



# -------     Login     ------- #
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	form = LoginForm(request.form)

	if request.method == 'POST':
		uname = request.form['username']
		pword = generate_password_hash(request.form['password'])

		if form.validate_on_submit():
			userSelected = select_user(uname)
			if request.form['username'] != userSelected[0] or request.form['password'] != userSelected[1]:
				error = 'Invalid Credentials. Please try again.'
			else:
				session['logged_in'] = True
				flash('You were logged in!')
				return redirect(url_for('home'))
		else:
			render_template('login.html', form=form, error=error)
	return render_template('login.html', form=form, error=error)



# -------     Logout     ------- #
@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	flash('You were just logged out!')
	return redirect(url_for('welcome'))



# -------     Error Handler     ------- #
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')



if __name__ == '__main__':
	app.run(debug = True)