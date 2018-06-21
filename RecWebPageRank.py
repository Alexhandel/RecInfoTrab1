# -*- coding: utf-8 -*-
#trabalho de Recuperação da Informação sobre Page Rank
#Autor: Alex Pungartnik Handel
import numpy as np

#parametros
beta=0.8
treshold=0.0001    

#modelagem do grafo como matriz de incidencia
pageMatrix=[[0,0.5,0.5,0],
			[0,0,1,0],
			[1,0,0,0],
			[0,0,1,0]]

T=len(pageMatrix)

def PageRank(pageMatrix):
	 
	initialMatrix=np.array(pageMatrix)
	#print initialMatrix

	jumpMatrix=np.ones([T,T])*((1-beta)/T)

	randomMatrix=jumpMatrix+(beta*initialMatrix)
	#print randomMatrix

	initialValues=np.array([1.0/float(T) for i in range(T)])
	

	#convergencia
	diff=10
	nextV=initialValues.copy()
	while diff>treshold:
		temp=nextV.copy()
		nextV=np.dot(nextV,randomMatrix)
		diff=max(np.square(nextV-temp))
		print diff, "\n", nextV, "\n"

	print "FINAL RESULT:\n", nextV


	pass
     
#Execução começa aqui
print 'START\n'   
PageRank(pageMatrix)