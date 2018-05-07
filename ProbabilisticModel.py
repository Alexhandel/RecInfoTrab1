# -*- coding: utf-8 -*-
#trabalho de Recuperação da Informação
#Autor: Alex Pungartnik Handel
import numpy as np

K1=1
b=0.75

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
def buildWordList(docList, query):
	wordList=[]
	list1=list(docList)
	list1.append(*query)
	for doc in list1:
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


	wordList=buildWordList(finalDocList, query)
	wordList.sort()

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

def calculateTF(terms, documents, query):
	print "\n*************\n", terms
	tfMatrix=[]
	documents.append(*query)
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

def calculateIDF(terms, documents, query):
	idfMatrix=[]
	documents.append(*query)
	ndocs=len(documents)
	for word in terms:
		frequencies=[]
		count=0
		for doc in documents:
			if word in doc: count+=1
		if count==0:
			idf=0
		else:
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

def tfIdf(terms, documents, query):
	tfMatrix = calculateTF(terms, documents, query)
	print "\n===========\ntf-matrix\n", np.matrix(tfMatrix)
	idfMatrix = calculateIDF(terms, documents, query)
	print "\n===========\nidf-matrix\n", np.matrix(idfMatrix).transpose()
	tfidf=calculateTfIdf(tfMatrix,idfMatrix)
	print "\n===========\ntfidf-matrix\n", tfidf
	return tfidf

def computeVectorSimilarity(d,q):
	dnorm=np.linalg.norm(d)
	qnorm=np.linalg.norm(q)
	dotproduct=np.dot(d.tolist()[0],q.tolist()[0])
	sim = dotproduct/(dnorm*qnorm)
	return sim

def calculateRankingsTFIDF(tfidf):
	TfIdfMatrix=np.matrix(tfidf)
	queryLine=TfIdfMatrix.transpose()[TfIdfMatrix.shape[1]-1]
	documentLines = np.delete(TfIdfMatrix.transpose(),TfIdfMatrix.shape[1]-1,0)
	simlist=[]
	for line in documentLines:
		similarity=computeVectorSimilarity(line,queryLine)
		simlist.append(similarity)
	indexedSimilarities=dict(enumerate(simlist))
	return indexedSimilarities

def VectorSpaceModelImplementation(docList, separators, stopwords, query):
	print docList,separators,stopwords,query
	finalDocList=tokenize(docList,separators)
	finalQuery=tokenize(query,separators)


	finalDocList=removeStopwords(finalDocList,stopwords)
	finalQuery=removeStopwords(finalQuery,stopwords)


	wordList=buildWordList(finalDocList,query)
	wordList.sort()
	print finalDocList,finalQuery,wordList
	TfIdfMatrix = tfIdf(wordList, finalDocList,finalQuery)
	similarities = calculateRankingsTFIDF(TfIdfMatrix)
	ranking = sorted(similarities, key=similarities.get)
	print "\nRESULTADO DA CONSULTA:\n", [query1], "\n"
	c=1
	for rank in ranking[::-1]:
		print c, ": documento numero", rank+1
		print "Similaridade:", similarities[rank]
		print DOCS[rank], "\n"
		c+=1
	pass

def simbm25(document, incidence, wordList, query, avgDocLength, niList):
	similarity=0
	count=0
	for word in wordList:
		Ni=niList[count]
		freqij=incidence[count]
		numerator=(K1+1)*freqij
		denominator=K1*((1-b)+(b*len(document)/avgDocLength)) + freqij
		beta=numerator/denominator
		logTerm = np.log2((len(DOCS)-Ni+0.5)/(Ni+0.5))
		similarity+=beta*logTerm
		#print word, "\n", beta, "\n", logTerm, "\n", similarity
		count+=1
	return similarity

def calculateRankingsProbabilistic(documents,query,docIncidence, wordList):
	finalRankings =[]
	docLengthList=[]
	for doc in documents:
		docLengthList.append(len(doc))
	avgDocLen=np.mean(docLengthList)
	print "AVERAGE DOC LENGTH: ", avgDocLen    

	documentFrequencies = []
	for word in wordList:
		count=0
		for doc in documents:
			if word in doc: count+=1
		documentFrequencies.append(count)
	print "DOCUMENT FREQUENCIES: ", documentFrequencies


	count=0
	for doc in documents:
		similarity=simbm25(doc, docIncidence[count], wordList, query, avgDocLen, documentFrequencies)
		finalRankings.append(similarity)
		count+=1
	finalRankings.sort()
	return finalRankings

def probabilisticModelImplementation(docList, separators, stopwords, query):
	print docList
	finalDocList=tokenize(docList,separators)
	finalQuery=tokenize(query,separators)

	finalDocList=removeStopwords(finalDocList,stopwords)
	finalQuery=removeStopwords(finalQuery,stopwords)

	wordList=buildWordList(finalDocList,finalQuery)
	wordList.sort()

	docIncidenceMatrix=buildIncidenceMatrix(finalDocList, wordList)
	queryIncidenceMatrix=buildIncidenceMatrix(finalQuery, wordList)

	print finalDocList, "\n--------\n", finalQuery, "\n--------\n", wordList, "\n--------\n", np.matrix(docIncidenceMatrix), "\n--------\n", queryIncidenceMatrix

	rankings = calculateRankingsProbabilistic(finalDocList,finalQuery,docIncidenceMatrix,wordList)
	print rankings   
	similarities=dict(enumerate(rankings))    
	ranking = sorted(similarities, key=similarities.get)
	print "\nRESULTADO DA CONSULTA:\n", [query1], "\n"
	c=1
	for rank in ranking[::-1]:
		print c, ": documento numero", rank+1
		print "Similaridade:", similarities[rank]
		print DOCS[rank], "\n"
		c+=1
	pass

#PROGRAMA COMEÇA EXECUÇÃO AQUI
print 'START\n'
#booleanModelImplementation(DOCS,separators1,stopwords1,[query1])
#VectorSpaceModelImplementation(DOCS,separators1,stopwords1,[query1])
probabilisticModelImplementation(DOCS,separators1,stopwords1,[query1])
