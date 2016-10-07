# coding:utf-8
from flask import Blueprint, render_template, request, jsonify, redirect, flash, session, current_app
from libs.decode import deinsert
from libs.encode import get
import cv2, os
from numpy import *
from PIL import Image

main_action = Blueprint('main_action', __name__)


class dealImage:
	def __init__(self):
		self.image = 'static/assets/Image.png'
		self.logo = 'static/assets/Logo.png'

	def insert(self):
		R, G, B = [get(self.image, self.logo, channel) for channel in ['R', 'G', 'B']]

		result = cv2.merge([B, G, R])

		cv2.imwrite('static/dist/after.png', result)

	def extract(self):
		R, G, B = [deinsert(self.image, self.logo, 'static/extract/upload/Lenna.png', channel) for channel in ['R', 'G', 'B']]
		result = cv2.merge([B, G, R])
		cv2.imwrite('static/extract/dist/logo.png', result)

	def rotate(self):
		rotate = cv2.imread('static/dist/after.png')

		rows, cols = rotate.shape[:2]
		M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 10, 1)
		dst = cv2.warpAffine(rotate, M, (cols, rows))
		cv2.imwrite('static/dist/after.png', dst)

	def slice_img(self, src, dir):
		img = cv2.imread(src)
		height, width = img.shape[:2]
		LU = img[0:height / 2, 0:width / 2]  # Crop from x, y, w, h -> 100, 200, 300, 400
		# NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]

		cv2.imwrite(dir+'/lu.png', LU)
		LD = img[256:height, 0:width / 2]
		cv2.imwrite(dir+'/ld.png', LD)

		RU = img[0:height / 2, width / 2:width]
		cv2.imwrite(dir+'/ru.png', RU)

		RD = img[height / 2:height, width / 2:width]
		cv2.imwrite(dir+'/rd.png', RD)

	def slice_insert(self):
		self.slice_img('static/assets/Image.png', 'static/assets/slice')
		img = cv2.imread('static/assets/Image.png')
		height, width = img.shape[:2]
		logo = cv2.imread(self.logo)
		logox1 = cv2.resize(logo, (height / 4, width / 4))
		cv2.imwrite('static/assets/_logo.png', logox1)
		_images = ['static/assets/slice/'+i for i in os.listdir('static/assets/slice/')]
		results = []
		for _img in _images:
			R, G, B = [get(_img, 'static/assets/_logo.png', channel) for channel in ['R', 'G', 'B']]
			result = cv2.merge([B, G, R])
			results.append(result)

		cv2.imwrite('static/assets/dist/modules/ld.png', results[0])
		cv2.imwrite('static/assets/dist/modules/lu.png', results[1])
		cv2.imwrite('static/assets/dist/modules/rd.png', results[2])
		cv2.imwrite('static/assets/dist/modules/ru.png', results[3])
		LD = cv2.imread('static/assets/dist/modules/ld.png')
		LU = cv2.imread('static/assets/dist/modules/lu.png')
		RD = cv2.imread('static/assets/dist/modules/rd.png')
		RU = cv2.imread('static/assets/dist/modules/ru.png')

		left_part = concatenate((LU, LD), axis=0)
		right_part = concatenate((RU, RD), axis=0)

		result = concatenate((left_part, right_part), axis=1)

		cv2.imwrite('static/assets/dist/after.png', result)

	def slice_extract(self):
		self.slice_img('static/extract/block/upload/Lenna.png', 'static/extract/block/modules')
		before_modules = os.listdir('static/assets/slice')
		modules = ['static/assets/slice/'+i for i in before_modules]
		_modules = ['static/extract/block/modules/'+i for i in before_modules]
		options = {}

		for i in xrange(4):
			options[modules[i]] = _modules[i]

		for _img in modules:
			R, G, B = [deinsert(_img, 'static/assets/_logo.png', options[_img], channel) for channel in ['R', 'G', 'B']]
			result = cv2.merge([B, G, R])
			cv2.imwrite('static/extract/block/dist/logo.'+_img[20:], result)


