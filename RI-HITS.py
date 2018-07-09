# -*- coding: utf-8 -*-
#trabalho de Recuperação da Informação de implementação do HITS
#Autor: Alex Pungartnik Handel
import numpy as np    
   
#modelagem do grafo como matriz de incidencia
pageMatrix=[[0,1,1,0],
			[0,0,1,0],
			[1,0,0,0],
			[0,0,1,0]]
#numero de iterações
k=650
   
#função que calcula os valores de hub
def getHubValues(matrix, values):
	#checagem de erro na entrada
	if len(matrix)!=len(values):
		print "ERROR"
		return 0

	results=np.zeros(len(matrix))
	#somatorio dos valores de authority
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			if matrix[i][j]>0: results[i]+=values[j]
	return results

#função que calcula os valores de authority
def getAuthorityValues(matrix, values):
	#checagem de erro na entrada
	if len(matrix)!=len(values):
		print "ERROR"
		return 0
	#transposição da matriz para pegar os que apontam para pagina ao inves dos que são apontados
	newMatrix = np.transpose(matrix)

	results=np.zeros(len(matrix))
	#somatorio dos valores de hub
	for i in range(len(matrix)):
		for j in range(len(newMatrix[i])):
			if newMatrix[i][j]>0: results[i]+=values[j]
	return results

def iterate(G,k):
	n=len(G)
	#inicia valores de hub e authority como 1
	hubValues=np.ones(n)
	authorityValues=np.ones(n)

	#iteração
	for i in range(k):
		#aplica a operação I
		hubValues=getHubValues(G,authorityValues.copy())
		#aplica a operação O
		authorityValues=getAuthorityValues(G,hubValues.copy())
		#normalização
		hubValues=hubValues/np.linalg.norm(hubValues)
		authorityValues=authorityValues/np.linalg.norm(authorityValues)
	print "\nRESULTS:\n"
	print "HUB", hubValues
	print "AUTHORITY", authorityValues

	pass


#programa começa aqui
iterate(pageMatrix,k)
