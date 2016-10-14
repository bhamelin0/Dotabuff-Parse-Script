nameList = []

with open("SampleCSV.csv") as f:
	for line in f:
		words = line.split(",")
		hero = words[5]
		
		found = False
		for names in nameList:
			if(hero == names):
				found = True
				break
				
		
		if (found == False):
			nameList.append(hero)
		
	nameList.sort()
	
	outputFile = open('HeroArray.csv', 'w')
	
	for item in nameList:
		outputFile.write("%s," % item)
	
	outputFile.write("\n")
	
outputArray = []
