# Graphable.py
# 'An application for logging and visualising data'
# Michael Harmer, 2013

# complete: 
# - create and add values to dataset
# - export dataset to file, import dataset from file

# todo:
# - gui design including most important features
# - PyQt tutorial

#notes:
#possibly just design a nice console-based gui
#then use turtle graphics to display graphs for simplicity/portability


import pickle

class Dataset:
	def __init__(self, name, desc):
		self.name = name
		self.desc = desc
		self.values = []

	def addValue(self, value):
		self.values.append(value);

	def printDataset(self):
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
	if isinstance(dataset, Dataset): # is actually a Dataset
		if dataset.name not in DATA: # has a unique name property	
			print(dataset.name,"unique, adding")
			DATA[dataset.name] = dataset
		else:
			print("!",dataset.name,"not unique, did not add")
	else:
		print("! addDataset was not passed a Dataset")

def exportDataset(datasetName): 
	""" pass a Dataset instance """
	f = open((datasetName.name+".pkl"), 'wb')
	pickle.dump(datasetName, f)
	f.close()
	print(datasetName.name,"exported")

def importDataset(datasetName):
	""" pass the name string of a Dataset """
	# checks for existing dataset, overwriting old dataset etc.
	# check that datasetName and fileName is a string
	# check that fileName is legit
	f = open((datasetName+".pkl"), 'rb')
	print("Importing dataset...")
	addDataset(pickle.load(f))
	f.close()	

def createGraph(*args):
	# write the datasets to a .jpg then display .jpg
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

# pickle testing
#exportDataset(test1, "f.txt") # works

#del test1

#importDataset(test1, "f.txt")
#print(test1.name)


#if __name__ == "__main__":
#	main()