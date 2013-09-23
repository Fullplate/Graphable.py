# Graphable.py
# An application for logging and graphing data.
# Written for Python 3
# Michael Harmer, 2013

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
		self.globwin = None

	def addDataset(self, newDataset):
		""" add a dataset to the graph """
		if len(self.sets) < self.maxSets:

			self.sets.append(newDataset)
			print("Added \'"+newDataset.name+"\'. "+str(len(self.sets))+"/" \
				+str(self.maxSets)+" datasets allocated.")
		else:
			print("! Maximum amount of datasets for graph reached.")

	def display(self):
		""" view a representation of the graph using turtle graphics """

		if len(self.sets) == 0:
			print("! Graph contains no datasets.")
			return

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
		self.displaySaveButton(turt)
		turt.pu()
		turt.setpos(-270, 360) # place arrow in a nice location

		self.globwin = win # set class-wide handle for the click handler function
		win.onclick(self.handleClick)

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
		t.write(self.name, font=('Arial', 24, 'normal'))

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

	def displaySaveButton(self, t):
		""" display the save button """
		t.pu()
		t.setpos(150, 340)
		t.pd()
		t.setpos(150, 380)
		t.setpos(300, 380)
		t.setpos(300, 340)
		t.setpos(150, 340)
		t.pu()
		t.setpos(161, 345)
		t.pd()
		t.write("SAVE .SVG", font=('Arial', 18, 'normal'))

	def handleClick(self, x, y):
		""" determine if button was clicked on, if so save canvas to .svg """
		if x >= 150 and x <= 300 and y >= 340 and y <= 380:
			canvasvg.saveall(self.name+".svg", self.globwin._canvas)
			print("Graph saved to .svg file! Check the Graphable directory.")

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
			print("\'"+dataset.name+"\' unique, adding.")
			DATA[dataset.name] = dataset
		else:
			print("! \'"+dataset.name+"\' not unique, did not add.")
	else:
		print("! addDataset was not passed a Dataset.")

def exportDataset(datasetName): 
	""" pickle an save a dataset, pass a dataset name string """
	f = open((datasetName+".pkl"), 'wb')

	if datasetName in DATA:
		pickle.dump(DATA[datasetName], f)
		print("\'"+datasetName+"\' exported.")
	else:
		print("! \'"+datasetName+"\' does not exist.")
	f.close()

def importDataset(datasetName):
	""" import a pickled dataset, pass a dataset name string """
	f = open((datasetName+".pkl"), 'rb')	
	addDataset(pickle.load(f))
	f.close()

# DATA holds Dataset instances, mapping dataset name:instance
DATA = {}

# PROGRAM ENTRY
def main():
	print("\_/* Graphable *\\_/")
	print("commmands: help, menu, dataset, graph, import, export, quit")

	# Main input loop
	inp = input("menu > ")
	while inp != "quit":
		if inp == "help":
			print("menu - return to main menu at any point")
			print("dataset - create or select an existing dataset")
			print("graph - create a new graph")
			print("import, export - save/load datasets. Warning: overwrites.")

		# Dialog for creating or selecting a dataset and adding data points
		elif inp == "dataset":
			inp = input("Dataset name (new or existing) > ")
			newPoints = []
			if inp != "menu":
				name = inp	
				found = False			
				# check if it's an existing dataset
				if name in DATA:
					found = True
					instance = name

				# get data points
				inp = input("1-10 to add data, menu to finish > ")
				while inp != "menu":
					try:
						numericInp = int(inp) # will throw exception if non-numeric
						if numericInp in range(1, 11):
							newPoints.append(numericInp)
							print("Data point added.")
						else:
							raise Exception() # manually raise exception if out of accepted range
					except:
						print("Invalid input.")
					inp = input("1-10 to add data, menu to finish > ")

				# user is done adding points
				if (found): # add points to the existing dataset
					for p in newPoints:
						DATA[name].addValue(p)
					print("Dataset \'"+name+"\' updated.")
				else: # create a new dataset and add points to it, then add it
					new = Dataset(name,"")
					for p in newPoints:
						new.addValue(p)
					addDataset(new)

		# Dialogue for creating a graph, adding datasets to it and displaying it
		elif inp == "graph":
			inp = input("Enter graph name > ")
			if inp != "menu":
				new = Graph(inp)
				inp = input("Enter dataset name to add, then \'display\' > ")
				while inp != "menu":
					if inp == "display":
						new.display()
					else: # locate dataset and add to graph -0 change to dict method
						gotInstance = False
						for i in DATA:
							if DATA[i].name == inp:
								instance = DATA[i]
								gotInstance = True
						if gotInstance:
							new.addDataset(instance)
						else:
							print("! dataset does not exist.")						
					inp = input("Enter dataset name to add, then \'display\' > ")	

		# Dialogue for pickling to file
		elif inp == "export":
			inp = input("Enter dataset name to export > ")
			if inp != "menu":
				exportDataset(inp)

		# Dialogue for unpickling
		elif inp == "import":
			inp = input("Enter dataset name to import > ")
			if inp != "menu":
				importDataset(inp)

		elif inp != "menu":
			print("Command not recognized.")

		print("commmands: help, menu, dataset, graph, import, export, quit")
		inp = input("menu > ")	

if __name__ == "__main__":
	main()