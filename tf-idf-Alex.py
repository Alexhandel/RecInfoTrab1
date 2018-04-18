# -*- coding: utf-8 -*-
#trabalho de Recuperação da Informação 
#Autor: Alex Pungartnik Handel   
import numpy as np


DOCS=['O peã e o caval são pec de xadrez. O caval é o melhor do jog.',
'A jog envolv a torr, o peã e o rei.',
'O peã lac o boi',
'Caval de rodei!',
'Polic o jog no xadrez.']

stopwords1=['','a', 'o', 'e', 'é', 'de', 'do', 'no','são']

separators1=[' ',',','.','!','?']

query1='xadrez peã caval torr'


#função que tokeniza os termos e normaliza pra caixa baixa  
def tokenize(documents,separators):
	result=[]
	for doc in documents: 
		doc=doc.lower()
		for sep in separators:
			doc=doc.replace(sep," ")
		doc=doc.split(" ")
		result.append(doc)
	

	return result

#função que remove stopwords
def removeStopwords(documents,stopwords):
	result=[]
	for doc in documents:
		temp=[]
		for token in doc:
			if token not in stopwords:
				temp.append(token)
		result.append(temp)
	return result
	pass

#função que cria uma lista dos termos únicos ao longo de todo os documentos
def buildWordList(docList):
	wordList=[]
	for doc in docList:
		for word in doc:
			if word not in wordList:
				wordList.append(word)
	return wordList
	pass


def buildIncidenceMatrix(documents,wordList):
	iMatrix=[]
	for doc in documents:
		line=[]
		for word in wordList:
			line.append(doc.count(word))
		iMatrix.append(line)
	return iMatrix
	pass



def booleanModelImplementation(docList,separators,stopwords,query):
	print docList,separators,stopwords,query
	finalDocList=tokenize(docList,separators)
	finalQuery=tokenize(query,separators)
	

	finalDocList=removeStopwords(finalDocList,stopwords)
	finalQuery=removeStopwords(finalQuery,stopwords)

	
	wordList=buildWordList(finalDocList)

	docIncidenceMatrix=buildIncidenceMatrix(finalDocList, wordList)
	queryIncidenceMatrix=buildIncidenceMatrix(finalQuery, wordList)
	 
	print "consulta: ", query1
	print "Tipo de consulta: OR"
	wordIndex=0
	resultIndexList=[]
	for element in queryIncidenceMatrix[0]:
		if element>0:
			docIndex=0
			for line in docIncidenceMatrix:
				if line[wordIndex]>0:
					if docIndex not in resultIndexList:
						resultIndexList.append(docIndex)
				docIndex+=1
		wordIndex+=1		
	if resultIndexList==[]:
			print "nenhum documento corresponde a consulta"
	else:
		for index in resultIndexList:
			print DOCS[index]

	print "\nTipo de consulta: AND"
	wordIndex=0
	resultIndexList=[]
	queryRelevantindexList=[]
	for element in queryIncidenceMatrix[0]:
		if element>0:
			if wordIndex not in queryRelevantindexList:
				queryRelevantindexList.append(wordIndex)
		wordIndex+=1
	docIndex=0		
	for line in docIncidenceMatrix:
		isResult=True
		for index in queryRelevantindexList:
			if line[index]==0:
				isResult=False
		if isResult:
			resultIndexList.append(docIndex)
		docIndex+=1
	if resultIndexList==[]:
			print "nenhum documento corresponde a consulta"
	else:
		for index in resultIndexList:
			print DOCS[index]
	
	pass        

def calculateTF(terms, documents):
	print "\n*************\n", terms
	tfMatrix=[]
	for doc in documents: 
		print doc
		frequencies=[]
		for word in terms:
			count=doc.count(word)
			tf=0
			if count>0:
				tf=1+np.log2(count)
			frequencies.append(tf)
		tfMatrix.append(frequencies)	
	return tfMatrix

def calculateIDF(terms, documents):
	idfMatrix=[]
	ndocs=len(documents)
	for word in terms: 
		frequencies=[]
		count=0
		for doc in documents:
			if word in doc: count+=1
		idf=np.log2(float(ndocs)/float(count))
		idfMatrix.append(idf)
	return idfMatrix

def calculateTfIdf(tf,idf):
	tfMatrix=tf
	idfMatrix=idf
	tfIdf=[]
	for line in tfMatrix:
		j=0
		for element in line:
			line[j]=line[j]*idfMatrix[j]
			j+=1
		tfIdf.append(line) 
	return np.matrix(tfIdf).transpose()

def tfIdf(terms, documents):
	tfMatrix = calculateTF(terms, documents)
	print "\n===========\ntf-matrix\n", tfMatrix
	idfMatrix = calculateIDF(terms, documents)
	print "\n===========\nidf-matrix\n", idfMatrix
	tfidf=calculateTfIdf(tfMatrix,idfMatrix)
	print "\n===========\ntfidf-matrix\n", tfidf
	return 0

def TFIDFImplementation(docList, separators, stopwords, query):
	print docList,separators,stopwords,query
	finalDocList=tokenize(docList,separators)
	finalQuery=tokenize(query,separators)
	

	finalDocList=removeStopwords(finalDocList,stopwords)
	finalQuery=removeStopwords(finalQuery,stopwords)

	
	wordList=buildWordList(finalDocList)
	print finalDocList,finalQuery,wordList
	tfIdfMatrix = tfIdf(wordList, finalDocList)


	pass


#PROGRAMA COMEÇA EXECUÇÃO AQUI
print 'START\n'
#booleanModelImplementation(DOCS,separators1,stopwords1,[query1]) 
TFIDFImplementation(DOCS,separators1,stopwords1,[query1])
