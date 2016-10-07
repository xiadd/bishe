# coding: utf-8
from flask import Flask, render_template, request, jsonify, session, redirect, current_app, flash
from flask.ext.bootstrap import Bootstrap
from pymongo import MongoClient
from jinja2 import TemplateNotFound

from views.insert import insert
from views.main import dealImage

client = MongoClient()
db = client.users
collection = db.userinfo

app = Flask(__name__)
app.debug = True
app.secret_key = 'xiadd'
Bootstrap(app)
# routes
app.register_blueprint(insert, url_prefix='/result')


@app.route('/')
def index():
	if 'username' in session:
		return render_template('index.html', username=session['username'])
	return render_template('index.html')


@app.route('/main', methods=['GET', 'POST'])
def main():
	if 'username' not in session:
		return '请<a href="/login">返回</a>登录'
	if request.method == 'GET':
		return render_template('main.html', url='/')
	if request.method == 'POST':

		with open('static/assets/Image.png', 'w') as f:
			map(f.write, request.files.get('uploadImage'))
		with open('static/assets/Logo.png', 'w') as l:
			map(l.write, request.files.get('uploadLogo'))
		_insert = dealImage()
		if request.form.get('block') is not None:
			_insert.slice_insert()
			return redirect('/result/block')
		_insert.insert()
		return redirect('/result')


@app.route('/main/block', methods=['GET', 'POST'])
def main_block():
	if 'username' not in session:
		return '请<a href="/login">返回</a>登录'
	if request.method == 'GET':
		return render_template('main.html', url='/block')
	if request.method == 'POST':
		print request.files
		with open('static/assets/Image.png', 'w') as f:
			map(f.write, request.files.get('uploadImage'))
		with open('static/assets/Logo.png', 'w') as l:
			map(l.write, request.files.get('uploadLogo'))
		_insert = dealImage()
		_insert.slice_insert()
		return redirect('/result/block')


@app.route('/register', methods=['POST'])
def register():
	if request.method == 'POST':
		existed = collection.find({'username': request.form['username']})
		if len(list(existed)) != 0:
			flash('user has existed')
			return redirect('/')

		collection.insert_one({'username': request.form['username'], 'password': request.form['password']})
		session['username'] = request.form['username']
		return redirect('/main')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		result = collection.find_one({'username': username})
		if result is not None:
			if(result['password'] == password):
				session['username'] = username
				return redirect('/')
			else:
				flash('error password')
				return redirect('/login')
		else:
			flash("user does't exist")
			return redirect('/')
	return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
	del session['username']
	return redirect('/')


@app.route('/extract', methods=['GET', 'POST'])
def extract():
	if 'username' not in session:
		return '请<a href="/login">返回</a>登录'
	if request.method == 'GET':
		return render_template('extract.html')

	if request.method == 'POST':
		with open('static/extract/upload/Lenna.png', 'w') as f:
			map(f.write, request.files.get('uploadImage'))
		extract_logo = dealImage()
		extract_logo.extract()
		return redirect('/result/extract')


@app.route('/extract/block', methods=['GET', 'POST'])
def slice_extract():
	if 'username' not in session:
		return '请<a href="/login">返回</a>登录'
	if request.method == 'GET':
		return render_template('extract.html', block='true')

	if request.method == 'POST':
		extract_logo = dealImage()
		with open('static/extract/block/upload/Lenna.png', 'w') as f:
			map(f.write, request.files.get('uploadImage'))
		extract_logo.slice_extract()

		return redirect('/result/extract/block')


if __name__ == '__main__':
	app.run(port=4000)