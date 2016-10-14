nameList = []

outputFile = open('FixedDuration.csv', 'w')

lineCount = 0

with open("SampleCSV.csv") as f:
	for line in f:
		words = line.split(",")
		duration = words[3]
		durationParts = duration.split(".")
		
		outputLine = ""
		
		hour = 0
		minute = 0
		seconds = 0
		
		if(len(durationParts)==3):
			hour = int(durationParts[0])
			minutes = int(durationParts[1])
			seconds = int(durationParts[2])
		
		if(len(durationParts)==2):
			minutes = int(durationParts[0])
			seconds = int(durationParts[1])
			
		if(len(durationParts)==1):
			seconds = int(durationParts[0])

		seconds +=minutes * 60
		seconds +=hour * 3600

		words[3] = str(seconds)

		for parts in words:
			outputLine += parts + ","
		
		lineCount+=1
		outputLine = outputLine[:-1]
		outputFile.write(outputLine)

				