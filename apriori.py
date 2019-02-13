import pandas as pd
from pandas import DataFrame as df
import numpy as np
from itertools import combinations
import sys
#input : data = [icecream,bread,sauce,bottled_water' u'\tmilk,icecream,bread'...]
#output :  map = {('bread', 'sauce'): 3,...}
def transform(data):
	candMap = {}
	for x in np.nditer(data, flags=['refs_ok'],op_flags=['readwrite']):
		trans = np.array(str(x).split(','))
		for i in np.nditer(trans):
			i = str(i).strip()
			if(len(i)>0):candMap[(i)] = candMap[i]+1 if i in candMap else 1
	return candMap
#input : data = [icecream,bread,sauce,bottled_water' u'\tmilk,icecream,bread'...], tupleItems = ('apple','banana',...)
#output : integer = 3
def getItemCount(data,tupleItems):
	counter = 0
	trans = np.array(data)
	tupleItems = np.array(tupleItems)
	for x in np.nditer(trans, flags=['refs_ok'],op_flags=['readwrite']):
		items = np.array(str(x).strip().split(','))
		checkArr = np.array([])
		for i in np.nditer(tupleItems):checkArr = np.append(checkArr, True if (i in items) else False)
		if((False in checkArr)==False):counter+=1
		checkArr=np.array([])
	return counter
#input : candidateMap = {('bread', 'sauce'): 3,...} , minSupport = 3
#output : map = {('bread', 'sauce'): 3,...}
def prune(candidateMap,minSupport):
	for key, value in candidateMap.items():
		if(value < minSupport):del candidateMap[key]
	return candidateMap
#input : table = [('banana', 'icecream')...] || ['apple','banana',...] , firstTable = ['apple','banana','icecream',...]
#output : map = {('bread', 'sauce'): 3,...}
def join(table,firstTable,minSupport):
	newTable = set([])
	for i in table:
		for j in firstTable:
			if ((j in i)==False):
				if(type(i) is str):a=np.array([i,j])
				else:a=np.array((i+(j,)))
				np.chararray.sort(a)
				newTable.add( tuple(a) )
	newTable=list(newTable)
	candMap={}
	for k in newTable:
		itemCount=getItemCount(data,k)
		if(itemCount>=minSupport):candMap[k]=itemCount
	return candMap
#input : {('bag', 'shoes', 'thermal_tshirt', 'winter_cap'): 2, ('bag', 'gloves', 'joggers', 'shoes'): 2}
#output: {('joggers', 'socks'): ('shoes',),...},{...}]
def generateRules(candMap):
	arr=[]
	for row in candMap:
		secondMap={}
		keyLength=1 #if keyLength is 1 generate key length of 1
		while (keyLength !=(len(row))):#run till keylength is size-1 of row
			rowList = list(combinations(row, keyLength))
			for item in rowList:
				data = (filter(lambda x : x not in item,row))
				secondMap[(item)] = data
			keyLength+=1
		arr.append(secondMap)
	return arr
#suprt x&y = occurance(x&y)/total_transactions
#confidence x -> y = occurance(x&y)/occurance(x)
#only print qualified association rules
def calculateConfidenceSupport(occuranceMap,allRules,minConfidence,freqKeys,total_transactions):
	rules=[]
	counter=0
	for row in allRules:
		occur = occuranceMap.get(freqKeys[counter])
		supp = round(occur/float(total_transactions),2)
		map={}
		for rule in row:
			alteredRule =  rule[0] if (len(rule)==1) else rule
			conf = round(occur / float(occuranceMap.get(alteredRule,None)),2)
			if(conf >= minConfidence  ):
				map[rule,row[rule]] = (supp,conf)
		counter+=1
		rules.append(map)
	return rules

argList = str(sys.argv)
if(len(sys.argv)<3):
	print("Please input 3 arguments:")
	print("1) Minimum Support(%)")
	print("2) Minimum Confidence(%)")
	print("3) Dataset(Amazon,BedBath,Columbia,Ikea,Stop&Shop)")
else:

	minSupport = float(sys.argv[1])
	minConfidence = float(sys.argv[2]) / 100.0
	letter = sys.argv[3][:1]
	dataset = ""
	if(letter == 'a'): dataset="amazon"
	elif(letter== 'b') : dataset="bedbath&beyond"
	elif(letter == 'c') : dataset="columbia"
	elif(letter == 'i') : dataset="ikea"
	else:
		print('Please selet a valid dataset')
		sys.exit(1)
	occuranceMap={}
	df = pd.read_excel('dataset/'+dataset+'.xlsx',header=None)
	data = np.array(df[1].values)#as_matrix
	firstTable = transform(data)
	totalTrans = len(data)
	occuranceMap = firstTable
	minSupport = (float(minSupport/100.0)*totalTrans)
	table = prune(firstTable,minSupport)
	#print(table)
	firstTableKeys = table.keys()
	freqItemSet = {}
	while len(table)>0:
		table = join(table.keys(),firstTableKeys,minSupport)
		if(table):
			occuranceMap.update(table)
			freqItemSet = table
			#print(table)
	allRules = generateRules(freqItemSet)
	associationRules = calculateConfidenceSupport(occuranceMap,allRules,minConfidence,freqItemSet.keys(),totalTrans)
	for row in associationRules:
		print(row)
