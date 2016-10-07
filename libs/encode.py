# coding:utf-8
import cv2, pywt
from numpy import *
from IPython import embed


def get(origin, logo, channel):
	origin_img = cv2.imread(origin)

	origin_B, origin_G, origin_R = cv2.split(origin_img)

	if(channel == 'R'):
		IcA1, [IcH1, IcV1, IcD1] = pywt.dwt2(origin_R, 'db1')
	elif(channel == 'G'):
		IcA1, [IcH1, IcV1, IcD1] = pywt.dwt2(origin_G, 'db1')
	else:
		IcA1, [IcH1, IcV1, IcD1] = pywt.dwt2(origin_B, 'db1')

	IcA2, [IcH2, IcV2, IcD2] = pywt.dwt2(IcA1, 'db1')
	'''奇异值分解'''
	[IcA_U, IcA_S, IcA_V] = linalg.svd(matrix(IcA2))
	[IcH_U, IcH_S, IcH_V] = linalg.svd(matrix(IcH2))
	[IcV_U, IcV_S, IcV_V] = linalg.svd(matrix(IcV2))
	[IcD_U, IcD_S, IcD_V] = linalg.svd(matrix(IcD2))


	# Logo处理
	logo_img = cv2.imread(logo)

	logo_B, logo_G, logo_R = cv2.split(logo_img)
	if(channel == 'R'):
		WcA1, [WcH1, WcV1, WcD1] = pywt.dwt2(logo_R, 'db1')
	elif(channel == 'G'):
		WcA1, [WcH1, WcV1, WcD1] = pywt.dwt2(logo_G, 'db1')
	else:
		WcA1, [WcH1, WcV1, WcD1] = pywt.dwt2(logo_B, 'db1')

	'''奇异值分解'''
	[WcA_U, WcA_S, WcA_V] = linalg.svd(WcA1)
	[WcH_U, WcH_S, WcH_V] = linalg.svd(WcH1)
	[WcV_U, WcV_S, WcV_V] = linalg.svd(WcV1)
	[WcD_U, WcD_S, WcD_V] = linalg.svd(WcD1)

	# 缩放矩阵
	key = 0.04
	# 数据处理
	tmp_LL = WcA_S*key
	tmp_HL = WcH_S*key
	tmp_LH = WcV_S*key
	tmp_HH = WcD_S*key

	# 含水印的R
	IkcA_S = IcA_S+tmp_LL
	IkcH_S = IcH_S+tmp_HL
	IkcV_S = IcV_S+tmp_LH
	IkcD_S = IcD_S+tmp_HH

	# 替换含水印的S,得到含水印的R
	IkcA2 = dot(IcA_U, dot(diag(IkcA_S), IcA_V))
	IkcH2 = dot(IcH_U, dot(diag(IkcH_S), IcH_V))
	IkcV2 = dot(IcV_U, dot(diag(IkcV_S), IcV_V))
	IkcD2 = dot(IcD_U, dot(diag(IkcD_S), IcD_V))

	# idwt2
	IkcA1 = pywt.idwt2([IkcA2,[IkcH2, IkcV2, IkcD2]], 'db1')

	Ik = pywt.idwt2([IkcA1,[IcH1, IcV1, IcD1]], 'db1')

	return Ik