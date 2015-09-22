from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from python_mysql_connect2 import connect
import hashlib
from form import LoginForm, GenderForm, SearchForm
from python_mysql_dbselect import select_user
from python_mysql_dbinsert import insert_user
import hashlib
import xml.etree.ElementTree as ET
import urllib2
import xmltodict
from xml.etree import ElementTree as etree

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



# -------     Home Route     ------- #
@app.route('/', methods=['GET', 'POST'])
#@login_required
def home():
	form = GenderForm(request.form)
	return render_template('index.html', form=form)



# -------     Search     ------- #
@app.route('/search', methods=['GET', 'POST'])
def search():
	form = SearchForm(request.form)
	return render_template('search.html', form=form)


# -------     Search Result    ------- #
@app.route('/result', methods=['GET', 'POST'])
@login_required
def result():
	form = SearchForm(request.form)
	url_search = 'http://www.behindthename.com/api/lookup.php?name='
	search_name = request.form['search']
	space_name = '&key='
	api_key = 'ya520550'
	print "hello, from the console"
	data = None
	result = None

	if request.method == 'POST':
		search_url = url_search + search_name + space_name + api_key
		file = urllib2.urlopen(search_url)
		data = file.read()
		file.close()
		data = xmltodict.parse(data)
		#result = data["response"]["name_detail"]["name"]
		#result += data["response"]["name_detail"]["gender"]
		result = []

		for z in data['response']['name_detail']:
			print z

		for i in data['response']['name_detail']['usages']['usage']:
			result.append(i['usage_code'])
			result.append(i['usage_full'])
			result.append(i['usage_gender'])


	else:
		print "Did not go through"
	return render_template('search.html', form=form, search=result)


# -------     Name Route     ------- #
@app.route('/name', methods=['GET', 'POST'])
def name():
	form = GenderForm(request.form)
	api_key = 'ya520550'
	url = 'http://www.behindthename.com/api/random.php?usage=ita&gender='
	space_name = '&key='
	data = None
	if request.method == 'POST':
		if request.form['gender'] == 'female':
			gender = 'f'
			htmlUrl = url + gender + space_name + api_key
			file = urllib2.urlopen(htmlUrl)
			data = file.read()
			file.close()
			data = xmltodict.parse(data)
			name_info = data["response"]["names"]["name"]
		else:
			gender = 'm'
			htmlUrl = url + gender + space_name + api_key
			file = urllib2.urlopen(htmlUrl)
			data = file.read()
			file.close()
			data = xmltodict.parse(data)
			name_info = data["response"]["names"]["name"]
	return render_template('index.html', form=form, names=name_info)


# -------     Welcome     ------- #
@app.route('/welcome')
def welcome():
	return render_template('welcome.html')



# -------     Registration Class     ------- #
@app.route('/register', methods=['GET', 'POST'])
def register():

	if request.method == 'POST':
		uname = request.form['username']
		pword = hashlib.md5(request.form['password']).hexdigest()
		emall = request.form['email']

		insert_user(uname, pword, emall)
		flash('Thanks for registering')
		return redirect(url_for('welcome'))
	return render_template('register.html')



# -------     List (Insert)     ------- #
# @app.route('/insert', methods=['GET', 'POST'])
# @login_required
# def add_to_list():
# 	if request.method = 'POST':
# 		bbname = request.form['']


# -------     Login     ------- #
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	form = LoginForm(request.form)

	if request.method == 'POST':
		uname = request.form['username']
		pword = request.form['password']

		if form.validate_on_submit():

			userSelected = select_user(uname)
			newPword = hashlib.md5(pword).hexdigest()

			userInfo = []

			for user in userSelected:
				userInfo.append(str(user))

			if str(uname) == userInfo[1] and str(newPword) == userInfo[2]:
				session['logged_in'] = True
				flash('You were logged in!')
				return redirect(url_for('home'))
			else:
				error = 'Invalid Credentials. Please try again.'
				
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