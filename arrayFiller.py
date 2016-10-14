nameList = []

outputFile = open('HeroArrayOut.csv', 'w')

with open('HeroArray.csv', 'r') as f:
	first_line = f.readline()
	nameList = first_line.split(",")

lineCount = 1

with open("FixedDuration.csv") as f:
	for line in f:
		words = line.split(",")
		skill = words[0]
		duration = words[3]
		winner = words[4]
		heroes = []
		heroes.append(words[5])
		heroes.append(words[19])
		heroes.append(words[33])
		heroes.append(words[47])
		heroes.append(words[61])
		heroes.append(words[88])
		heroes.append(words[102])
		heroes.append(words[116])
		heroes.append(words[130])
		heroes.append(words[144])

		outputLine = skill + "," + duration + "," + winner + ",";
		
		
		count = 0;
		for names in nameList:
			found = False
			for i in range(0,5):
				if(heroes[i]==names):
					outputLine += "1,"
					found = True
					count+=1
			for i in range(5,10):
				if(heroes[i]==names):
					outputLine += "-1,"
					found = True
					count+=1
			if(found == False):
				outputLine += "0,"
		
		if(count != 10):
			print("ERROR" + str(count) + " " + str(lineCount) +" " + duration + heroes[0] + winner + "\n")
		
		lineCount+=1
		outputLine = outputLine[:-1]
		outputFile.write(outputLine + "\n")

				