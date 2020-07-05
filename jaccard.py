#-*- coding:utf-8 -*-
import numpy as np 
import ProcessMatrix
import logging
logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s : %(message)s')

_JACCARD_METHODS = {'similarity':0,'distance':1}

def commatrix_to_matrix(matrix):
	'''
	将共现矩阵转化为普通矩阵
	'''
	title = matrix[0,1:]
	matrix = np.delete(matrix, 0, axis = 1)#删除第一列
	matrix = np.delete(matrix, 0, axis = 0)#删除第一行
	return matrix, title

def matrix_to_comatrix(matrix, title):
	'''
	将普通矩阵转化为共现矩阵
	'''
	matrix = matrix.astype('U10')
	matrix = np.insert(matrix, 0, values=title, axis=0)
	title = title.tolist()
	title.insert(0, '')
	title = np.array(title)
	matrix = np.insert(matrix, 0, values=title, axis=1)
	return matrix

def get_jaccard_similarity_matrix(matrix):
	'''
	计算jaccard相似度
	'''
	matrix = matrix.astype('int')
	diag_array = np.diag(matrix)#对角值

	matrixA = np.tile(diag_array, (diag_array.shape[0],1))
	matrixB = matrixA.T
	matrixC = matrixA + matrixB - matrix

	logging.info("success to get_jaccard_similarity_matrix...")

	return matrix / matrixC

def get_jaccard_distance_matrix(matrix):
	'''
	计算jaccard距离
	'''
	return 1 - get_jaccard_similarity_matrix(matrix) 

def get_jaccard_matrix(method = 'similarity'):
	if method not in _JACCARD_METHODS:
		raise ValueError("Invalid method: {0}".format(method))
	method_code = _JACCARD_METHODS[method]

	comatrix = ProcessMatrix.get_comatrix()#获取共现矩阵
	matrix, title = commatrix_to_matrix(np.array(comatrix))

	if method == 0:		
		matrix = get_jaccard_similarity_matrix(matrix) #jaccard相似性
	else:
		matrix = get_jaccard_distance_matrix(matrix) #jaccard距离

	jaccard_matrix = matrix_to_comatrix(matrix, title)
	return jaccard_matrix

def test():
	a = [['3','2','0','1'],
	 ['2','4','4','2'],
	 ['0','4','5','3'],
	 ['1','2','3','6']]

	b = np.array([['','a','b','c','d'],
	['a','3','2','0','1'],
	['b','2','4','4','2'],
	['c','0','4','5','3'],
	['d','1','2','3','6']])

	# title = np.array([['a','b','c','d']])

	# matrix = matrix_to_comatrix(a, title)
	# print(matrix)

	matrix, title = commatrix_to_matrix(b)
	print(matrix)
	print(title)
	print(type(title))
	print(title.shape)
	# c = matrix.astype('int')
	# print(c)
	matrix = get_jaccard_similarity_matrix(matrix)
	print(matrix)
	# matrix = matrix.astype('U10')
	# print(matrix)
	matrix = matrix_to_comatrix(matrix, title)
	print(matrix)

if __name__ == '__main__':
	# test()
	method = 'similarity'
	jaccard_matrix = get_jaccard_matrix(method)
	output_path = "../../建模数据/结果数据_jaccard/jaccard_{}.txt".format(method)
	ProcessMatrix.save_comatrix(jaccard_matrix, output_path = output_path)
