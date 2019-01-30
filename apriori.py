import pandas as pd
from pandas import DataFrame as df
import numpy as np

df = pd.read_excel('stop_shop.xlsx',header=None)
data = np.array(df.as_matrix([1]))
print(data)

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
		
		
		
		
		
		
		
	return



print(getCandidateMap(data))	