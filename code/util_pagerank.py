#-*- coding:utf-8 -*-
import numpy as np
from numpy import dot

def graphMove(a): # 计算transition matrix
	b = np.transpose(a) #为什么要transpose呢？我觉得matrix[i][j]=matrix[j][i] ? 是的
	# for i in range(a.shape[0]):
	# 	for j in range(a.shape[1]): 
	# 		print(a[i][j]==b[j][i]) #
	# 		print("------------------------------")
	c = np.zeros((a.shape), dtype = float)
	for i in range(a.shape[0]):
		for j in range(a.shape[1]): 
			if b[j].sum() == 0: #什么意思？？？ 他所在的group内的其他点到b[j]这个点的距离之和
				print("EXIST???")#我觉得这里不会有这种情况
				c[i][j] = 1.0 / (len(b[j]) * 1.0) # 如果j这个点与其他点没有link，所以就是随即拜访（点的数量）的概率，这样初始化对吗？也许应该是0，因为(1-p)*v这一项已经承担了extra的概率吧
			else:
				c[i][j] = (a[i][j] * 1.0) / (b[j].sum() * 1.0) # i点到j点的距离/group内的其他点到b[j]这个点的距离之和（如果这样想，我觉得这个矩阵计算的有问题？？？但也许因为所有边都是双向的所以问题不大？b[j]这个点到其他点的距离之和，这样想的话得到的是列所以没有问题。。）
	return c

def firstPr(c): # 初始化为1/n,确实只需要1列就足够了,n为group内点的个数
	pr = np.zeros((c.shape[0],1),dtype = float) 
	for i in range(c.shape[0]):
		pr[i] = float(1)/c.shape[0]
	return pr

def pageRank(p,m,v): # v是初始化为1/n的矩阵，m是经过计算的矩阵，p是一个参数（什么参数）
	flag = 1000
	# v=np.array([1,2])
	# z =np.array( [1,3])
	# print((z==v).all())
	# print(z==v)
	while((v == p*dot(m,v) + (1-p)*v).all()==False): #这个条件的意思是矩阵中如果有一项不相等
		v = p*dot(m,v) + (1-p)*v
		flag = flag - 1
		if flag == 0 and max(abs(v - (p*dot(m,v) + (1-p)*v))) < 0.0001: #convergence
			break
	return v