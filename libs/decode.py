# coding:utf-8
from __future__ import division
import cv2, pywt
from numpy import *
from encode import get


def deinsert(image, logo, after_image, channel):
	I = cv2.imread(image)
	B, G, R = cv2.split(I)

	if (channel == 'R'):
		IcA1, [IcH1, IcV1, IcD1] = pywt.dwt2(R, 'db1')
	elif (channel == 'G'):
		IcA1, [IcH1, IcV1, IcD1] = pywt.dwt2(G, 'db1')
	else:
		IcA1, [IcH1, IcV1, IcD1] = pywt.dwt2(B, 'db1')
	IcA2, [IcH2, IcV2, IcD2] = pywt.dwt2(IcA1, 'db1')

	# 奇异值变换
	[IcA_U, IcA_S, IcA_V] = linalg.svd(IcA2)
	[IcH_U, IcH_S, IcH_V] = linalg.svd(IcH2)
	[IcV_U, IcV_S, IcV_V] = linalg.svd(IcV2)
	[IcD_U, IcD_S, IcD_V] = linalg.svd(IcD2)

	# 含水印图像的处理

	img = cv2.imread(after_image)

	b, g, r = cv2.split(img)

	if (channel == 'R'):
		Ik = r
	elif (channel == 'G'):
		Ik = g
	else:
		Ik = b
	Ik_cA1, [Ik_cH1, Ik_cV1, Ik_cD1] = pywt.dwt2(Ik, 'db1')
	Ik_cA2, [Ik_cH2, Ik_cV2, Ik_cD2] = pywt.dwt2(Ik_cA1, 'db1')

	# 奇异值分解
	[Ik_cA_U, Ik_cA_S, Ik_cA_V] = linalg.svd(Ik_cA2)
	[Ik_cH_U, Ik_cH_S, Ik_cH_V] = linalg.svd(Ik_cH2)
	[Ik_cV_U, Ik_cV_S, Ik_cV_V] = linalg.svd(Ik_cV2)
	[Ik_cD_U, Ik_cD_S, Ik_cD_V] = linalg.svd(Ik_cD2)

	# 奇异值相减，提取水印
	Dk_cA2 = Ik_cA_S - IcA_S
	Dk_cH2 = Ik_cH_S - IcH_S
	Dk_cV2 = Ik_cV_S - IcV_S
	Dk_cD2 = Ik_cD_S - IcD_S

	# 计算关键值
	key = 0.04
	PCk_cA1 = Dk_cA2 / key
	PCk_cH1 = Dk_cH2 / key
	PCk_cV1 = Dk_cV2 / key
	PCk_cD1 = Dk_cD2 / key

	# 计算提取的水印
	logo_img = cv2.imread(logo)

	logo_B, logo_G, logo_R = cv2.split(logo_img)
	if (channel == 'R'):
		WcA1, [WcH1, WcV1, WcD1] = pywt.dwt2(logo_R, 'db1')
	elif (channel == 'G'):
		WcA1, [WcH1, WcV1, WcD1] = pywt.dwt2(logo_G, 'db1')
	else:
		WcA1, [WcH1, WcV1, WcD1] = pywt.dwt2(logo_B, 'db1')

	'''奇异值分解'''
	[WcA_U, WcA_S, WcA_V] = linalg.svd(WcA1)
	[WcH_U, WcH_S, WcH_V] = linalg.svd(WcH1)
	[WcV_U, WcV_S, WcV_V] = linalg.svd(WcV1)
	[WcD_U, WcD_S, WcD_V] = linalg.svd(WcD1)
	# 提取的水印
	Wk_cA1 = dot(WcA_U, dot(diag(PCk_cA1), WcA_V))
	Wk_cH1 = dot(WcH_U, dot(diag(PCk_cH1), WcH_V))
	Wk_cV1 = dot(WcV_U, dot(diag(PCk_cV1), WcV_V))
	Wk_cD1 = dot(WcD_U, dot(diag(PCk_cD1), WcD_V))
	# Wk_cA1 = WcA_U*diag(PCk_cA1)*WcA_V
	# Wk_cH1 = WcH_U*diag(PCk_cH1)*WcH_V
	# Wk_cV1 = WcV_U*diag(PCk_cV1)*WcV_V
	# Wk_cD1 = WcD_U*diag(PCk_cD1)*WcD_V

	Wk = pywt.idwt2([Wk_cA1, [Wk_cH1, Wk_cV1, Wk_cD1]], 'db1')
	Wk = matrix(Wk)
	return Wk
