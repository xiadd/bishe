from flask import Blueprint, render_template, request, jsonify, redirect, flash
insert = Blueprint('insert', __name__)


@insert.route('/')
def insert_action():
	return render_template('result.html', insert_result='dist/after.png')


@insert.route('/block')
def block_insert():
	return render_template('result.html', insert_result='assets/dist/after.png', blocked=True)


@insert.route('/extract')
def extract_action():
	return render_template('result.html', extract_result='extract/dist/logo.png')


@insert.route('/extract/block')
def block_extract():
	return render_template('result.html', extract_result='extract/block/dist/logo.ld.png')