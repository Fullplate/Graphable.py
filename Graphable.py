# Graphable.py
# 'An application for logging and visualising data'
# Written for Python 3, with a simple CLI and turtle graphics
# Michael Harmer, 2013

# basic functionality complete!
# - finish error checking/exceptions
# - do-whiles for input (cleaner code)
# - make it clearer that you use menu to cancel an operation, or go back to menu
# - graphs should be handled the same way as datasets - import/export feature, unique names shared
# - datasets and graphs need to be selectable and editable

import pickle
import turtle
import canvasvg

# DATA STRUCTURES
class Dataset:
	def __init__(self, name, desc):
		self.name = name
		self.desc = desc
		self.values = []

	def addValue(self, value):
		""" Add a data point to the dataset """
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
		self.colours = ["red","blue","green","orange","pink"]
		self.maxSets = len(self.colours)

	def addDataset(self, newDataset):
		""" add a dataset to the graph """
		if len(self.sets) < self.maxSets:
			self.sets.append(newDataset)
		else:
			print("! Maximum amount of datasets for graph reached.")

	def display(self):
		""" view a representation of the graph using turtle graphics """
		# setup
		turt = turtle.Turtle()
		win = turtle.Screen()
		turt.speed(10)
		turt.shape("arrow")

		# draw graph axis and labels in default colour (black), then the legend
		turt.width(2)
		self.displayAxis(turt)
		self.displayLabels(turt)
		turt.width(5)
		self.displayLegend(turt)		
		
		currIndex = 0 # use to rotate through colours
		turt.color(self.colours[currIndex])
		turt.width(3)

		# draw each dataset in a different colour
		for dataset in self.sets:
			self.displayDataset(turt, dataset)
			if (currIndex < 4):
				currIndex += 1
			turt.color(self.colours[currIndex])

		turt.color("black")

		canvasvg.saveall(self.name+".svg", win._canvas)

		win.exitonclick()

	def displayAxis(self, t):
		""" display the x and y axis  """
		# note: hardcoded to a 500x500 set of axis, origin at -250,-250
		t.pu()
		t.setpos(-250,-250)
		t.pd()
		t.setpos(-250, 250)
		t.pu()
		t.setpos(-250,-250)
		t.pd()
		t.setpos(250, -250)

	def displayLabels(self, t):
		""" display the title and axis labels """
		t.pu()
		t.setpos(-270, 260)
		t.pd()
		t.write("VALUE", font=('Arial', 12, 'normal'))
		t.pu()
		t.setpos(270, -255)
		t.pd()
		t.write("TIME", font=('Arial', 12, 'normal'))
		t.pu()
		t.setpos(-250, 340)
		t.pd()
		t.write(self.name, font=('Arial', 30, 'normal'))

	def displayDataset(self, t, dataset):
		""" draw a dataset on the axis - unoptimised for readability """
		# some setup
		numPoints = len(dataset.values)
		pointScale = 500 / 10 # 10 being the current highest possible val7		
		if numPoints == 1:
			timeScale = 500
		else:
			timeScale = 500 / (numPoints - 1) # because starts on the axis

		# generate coordinates from points
		coords = []
		for i in range(1, numPoints+1):
			x = -250 + ((i-1) * timeScale)			# x-axis, or time value
			y = -250 + (dataset.values[i-1] * pointScale)	# y-axis, or point value	
			coords.append([x,y])

		# run through coordinates and draw
		t.pu()
		t.setpos(coords[0][0], coords[0][1])
		t.pd()
		for i in range(1, numPoints):
			t.setpos(coords[i][0], coords[i][1])

		# hack for single valued datasets
		if numPoints == 1:
			for i in range(-250, 250, 10):				
				t.pu()
				t.setpos(i, -250 + dataset.values[0] * pointScale)
				t.pd()
				t.dot(3)

	def displayLegend(self, t):
		""" display the legends for each dataset """
		# for each dataset, draw a horizontal line below the graph in the matching colour
		# then write the dataset name next to that line
		lineY = -280 # starting y position for the legend
		lineX = [-250, -185, -170] # start of line, end of line, start of text

		for i in range(0, len(self.sets)):
			t.color(self.colours[i])
			currY = lineY - i * 25
			t.pu()
			t.setpos(lineX[0], currY)
			t.pd()
			t.setpos(lineX[1], currY)
			t.pu()
			t.setpos(lineX[2], currY - 8)
			t.pd()
			t.color("black")
			t.write(self.sets[i].name, font=('Arial', 12, 'normal'))

	def printGraph(self):
		""" print graph for debugging purposes """
		print("Graph:",self.name)
		for i in self.sets:
			i.printDataset()

# INTERFACE FUNCTIONS
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
	""" pickle an save a dataset, pass a a dataset name string """
	f = open((datasetName+".pkl"), 'wb')
	gotInstance = False
	for i in DATA:
		if DATA[i].name == datasetName:
			instance = DATA[i]
			gotInstance = True

	if gotInstance:
		pickle.dump(instance, f)
		f.close()
		print(datasetName,"exported")
	else:
		print("! dataset does not exist")

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

# DEV FUNCTIONS
def testAll():
	print()
	# Dataset testing
	#addDataset(Dataset("test1", "test dataset"))

	#exportDataset(DATA["test1"])
	#del DATA["test1"]
	#importDataset("test1")

	#for i in DATA:
	#	DATA[i].printDataset()

	# Graph testing
	#createGraph(test1, test2)

def debug():
	print("...\nDatasets:")
	for i in DATA:
		DATA[i].printDataset()

# DATA holds Dataset instances
DATA = {}
# GRAPHS holds Graph instances
GRAPHS = {}

# Program entry
def main():
	print("\_/* Graphable *\\_/")
	print("commmands: help, menu, mkd, mkg, import, export, quit")

	# Input loop
	inp = input("> ")
	while inp != "quit":
		if inp == "help":
			print("menu - return to main menu\nmkd, mkg - make dataset and graph")
			print("import, export - save and load dataset to/from file")

		# Dialog for creating a dataset and adding data points
		elif inp == "mkd":
			inp = input("Dataset name: ")
			if inp != "menu":
				new = Dataset(inp,"")
				
				inp = input("Enter 1-10 to add a data point: ")
				while inp != "menu":
					numericInp = int(inp)
					if (numericInp in range(1, 11)):
						new.addValue(numericInp)
						print("Data point added.")
					inp = input("Enter 1-10 to add a data point: ")
				addDataset(new)


		# Dialogue for creating a graph, adding datasets to it and displaying it
		elif inp == "mkg":
			inp = input("Enter graph name: ")
			if inp != "menu":
				new = Graph(inp)
				inp = input("Enter dataset to add, or type display: ")
				while inp != "menu":
					if inp == "display":
						new.display()
					else: # locate dataset and add to graph
						gotInstance = False
						for i in DATA:
							if DATA[i].name == inp:
								instance = DATA[i]
								gotInstance = True
						if gotInstance:
							new.addDataset(instance)
						else:
							print("! dataset does not exist")						
					inp = input("Enter dataset to add, or type display: ")	

		# Dialogue for pickling to file
		elif inp == "export":
			inp = input("Enter dataset name to export: ")
			if inp != "menu":
				exportDataset(inp)

		# Dialogue for unpickling
		elif inp == "import":
			inp = input("Enter dataset name to import: ")
			if inp != "menu":
				importDataset(inp)

		# Misc
		elif inp == "debug":
			debug()

		inp = input("> ")	

if __name__ == "__main__":
	main()