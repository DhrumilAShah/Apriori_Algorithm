import pandas as pd
from pandas import DataFrame as df
import numpy as np

df = pd.read_excel('stop&shop.xlsx',header=None)
data = np.array(df.as_matrix([1]))
#print(data)

def getCandidateMap(arr):
	candMap = {}
	for x in np.nditer(arr, flags=['refs_ok'],op_flags=['readwrite']):
		trans = np.array(str(x).split(','))
		for i in np.nditer(trans):
			i=str(i).strip()
			if i in candMap:
				candMap[i] = candMap[i]+1
			else:
				candMap[i]=1
	return candMap


def getSupport(data,*args):
	counter=0	
	trans = np.array(data)
	args = np.array(args)
	for x in np.nditer(trans, flags=['refs_ok'],op_flags=['readwrite']):
		items = np.array(str(x).strip().split(','))	
		checkArr=np.array([])
		for i in np.nditer(args):checkArr = np.append(checkArr, True if (i in items) else False)							
		if((False in checkArr)==False):counter+=1
		checkArr=np.array([])	
	return counter


#print(getCandidateMap(data))
#print()
print(getSupport(data,"apple","banana"))	
