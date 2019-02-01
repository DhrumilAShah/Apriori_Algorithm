import pandas as pd
from pandas import DataFrame as df
import numpy as np

df = pd.read_excel('dataset/stop&shop.xlsx',header=None)
data = np.array(df[1].values)#as_matrix
#print(data)

def transform(data):
	candMap = {}
	for x in np.nditer(data, flags=['refs_ok'],op_flags=['readwrite']):
		trans = np.array(str(x).split(','))
		for i in np.nditer(trans):
			i = str(i).strip()
			candMap[(i)] = candMap[i]+1 if i in candMap else 1
	return candMap

def getItemCount(data,*args):
	counter = 0
	trans = np.array(data)
	args = np.array(args)
	for x in np.nditer(trans, flags=['refs_ok'],op_flags=['readwrite']):
		items = np.array(str(x).strip().split(','))
		checkArr=np.array([])
		for i in np.nditer(args):checkArr = np.append(checkArr, True if (i in items) else False)
		if((False in checkArr)==False):counter+=1
		checkArr=np.array([])
	return counter

def prune(candidateMap,minSupport):
	for key, value in candidateMap.items():
		if(value < minSupport):del candidateMap[key]
	return candidateMap

def join(candidateKeys):
	candidateKeys = np.array(candidateKeys)
	arr = np.array([])
	counter = 0
	for y in np.nditer(candidateKeys[:-1]):
		for x in np.nditer(candidateKeys[:-2]):
			arr = np.append(arr,(candidateKeys[counter],candidateKeys[counter+1]))
		counter+=1
	print(arr)
	return


print(join(['as','bs','cs','ds']))
#print(transform(data))
#print(getItemCount(data,"apple","banana"))
