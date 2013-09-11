# Graphable.py
# 'An application for logging and visualising data'
# Michael Harmer, 2013

# complete: 
# - create and add values to dataset
# - export dataset to file, import dataset from file

# todo:
# - turtle graphics output for prototype
# - simple CLI

import pickle

class Dataset:
	def __init__(self, name, desc):
		self.name = name
		self.desc = desc
		self.values = []

	def addValue(self, value):
		""" Add a data point to the dataset"""
		self.values.append(value);

	def printDataset(self):
		""" print dataset for debugging purposes """
		print(self.name+": "+self.desc)
		for i in range(0, len(self.values)):
			print(i, self.values[i])

class Graph:
	def __init__(self, name):
		self.name = name
		self.sets = []

	def addDataset(set):
		self.sets.append(set)

def addDataset(dataset):
	""" create a new dataset with a unique name """ 
	if isinstance(dataset, Dataset): # is actually a Dataset
		if dataset.name not in DATA: # has a unique name property	
			print(dataset.name,"unique, adding")
			DATA[dataset.name] = dataset
		else:
			print("!",dataset.name,"not unique, did not add")
	else:
		print("! addDataset was not passed a Dataset")

def exportDataset(datasetName): 
	""" pickle an save a dataset, pass a a dataset object """
	f = open((datasetName.name+".pkl"), 'wb')
	pickle.dump(datasetName, f)
	f.close()
	print(datasetName.name,"exported")

def importDataset(datasetName):
	""" import a pickled dataset, pass a dataset name string """
	# checks for existing dataset, overwriting old dataset etc.
	# check that datasetName and fileName is a string
	# check that fileName is legit
	f = open((datasetName+".pkl"), 'rb')
	print("Importing dataset...")
	addDataset(pickle.load(f))
	f.close()	

def createGraph(*args):
	""" creates a visual representation of a number of passed dataset objects """
	for set in args:
		print(set.name)


DATA = {} # possibly make this not hardcoded

# Dataset testing
addDataset(Dataset("test1", "test dataset"))

exportDataset(DATA["test1"])
del DATA["test1"]
importDataset("test1")

for i in DATA:
	DATA[i].printDataset()

# Graph testing
#createGraph(test1, test2)

#if __name__ == "__main__":
#	main()