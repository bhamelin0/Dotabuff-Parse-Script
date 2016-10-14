#Reads in match data for DOTA 2 from dotabuff, and parses it such that it generates a .csv of the statistics of each hero in the match.
import http.client
import time
from html.parser import HTMLParser

def checkValid(tagList):
	if len(tagList) < 5:
		return 0
	if "SKILL:" not in tagList[0] or "All Pick" not in tagList[2] or "DURATION:" not in tagList[3] or "WINNER:" not in tagList[4] or "HERO:" not in tagList[5]:
		return 0
	if "RANK:Ranked Matchmaking" not in tagList[1] and "RANK:Normal Matchmaking" not in tagList[1]:
		return 0
	if len(tagList) != 171:
		return 0
	for lines in tagList:
		if "STAT:Abandoned" in lines:
			return 0
	return 1

class MyHTMLParser(HTMLParser):
	def __init__(self):
		self.tagList = []
		self.onHero = 0
		self.itemCount = 0
		self.heroCount = 0
		self.lineCount = 0
		self.summary = 0
		super().__init__()
		
	

	def handle_starttag(self, tag, attrs):
		self.lineCount += 1
		atts=""
		for t in attrs:
			atts += t[0]+t[1]
		out = (tag + " " + atts)
		if "a href/heroes/" in out and self.lineCount > 280:
			self.tagList.append("HERO:"+out)
			self.onHero = 1
			self.heroCount = self.heroCount + 1
			if self.heroCount == 6:
				self.summary = 0
				
		#else:
			#self.tagList.append("NO HERO:"+out)
			
	def handle_endtag(self, tag): 
		self.lineCount += 1
		out = ("Encountered an end tag :"+ tag)
		#self.tagList.append(out)
		
	def handle_data(self, data):
		self.lineCount += 1
		if self.heroCount == 0:
			if " Victory" in data:
				self.tagList.append("WINNER:"+data)
			if " Skill" in data:
				self.tagList.append("SKILL:"+data)
			if " Matchmaking" in data:
				self.tagList.append("RANK:"+data)
			if "All Pick" in data:
				self.tagList.append(data)
			if ":" in data:
				self.tagList.append("DURATION:"+data)
			
				
		elif self.onHero == 1:
			self.itemCount = self.itemCount + 1
			if self.itemCount > 1:
				self.tagList.append("STAT:"+data)
			if self.itemCount > 13:
				self.onHero = 0
				self.itemCount = 0
		else:
			if self.summary < 13:
				self.tagList.append("SUM:"+data)
				self.summary += 1
				
	def returnResults(self):
		return self.tagList

matchseed = 2198162911
speed = 10
runs = 1000
#Pull matchseed from settings
with open('DotaParseSettings.ini') as f:
	for line in f:
		matchseed = int(line)
		line = next(f)
		speed = int(line)
		line = next(f)
		runs = int(line)
print("Seconds between requesting:")
print(speed)
print("Match seed:")
print(matchseed)
print("Number of runs:")
print(runs)

lst = """Dotaboof"""

hdr= { 'User-Agent' : 'Readerererer by Raik' }
#http://www.dotabuff.com/matches/2197646225
h1 = http.client.HTTPConnection('www.dotabuff.com')

outputFile = open('MatchData.csv', 'wb')
outString = "Skill,Rank,Gametype,Duration,Winner,"
outString +="H1,H1LVL,H1K,H1D,H1A,H1KDA,H1Gold,H1LH,H1DN,H1XPM,H1GPM,H1HD,H1HH,H1TD,"
outString +="H2,H2LVL,H2K,H2D,H2A,H2KDA,H2Gold,H2LH,H2DN,H2XPM,H2GPM,H2HD,H2HH,H2TD,"
outString +="H3,H3LVL,H3K,H3D,H3A,H3KDA,H3Gold,H3LH,H3DN,H3XPM,H3GPM,H3HD,H3HH,H3TD,"
outString +="H4,H4LVL,H4K,H4D,H4A,H4KDA,H4Gold,H4LH,H4DN,H4XPM,H4GPM,H4HD,H4HH,H4TD,"
outString +="H5,H5LVL,H5K,H5D,H5A,H5KDA,H5Gold,H5LH,H5DN,H5XPM,H5GPM,H5HD,H5HH,H5TD,"
outString +="SUM1LVL,SUM1K,SUM1D,SUM1A,SUM1KDA,SUM1Gold,SUM1LH,SUM1DN,SUM1XPM,SUM1GPM,SUM1HD,SUM1HH,SUM1TD,"

outString +="H6,H6LVL,H6K,H6D,H6A,H6KDA,H6Gold,H6LH,H6DN,H6XPM,H6GPM,H6HD,H6HH,H6TD,"
outString +="H7,H7LVL,H7K,H7D,H7A,H7KDA,H7Gold,H7LH,H7DN,H7XPM,H7GPM,H7HD,H7HH,H7TD,"
outString +="H8,H8LVL,H8K,H8D,H8A,H8KDA,H8Gold,H8LH,H8DN,H8XPM,H8GPM,H8HD,H8HH,H8TD,"
outString +="H9,H9LVL,H9K,H9D,H9A,H9KDA,H9Gold,H9LH,H9DN,H9XPM,H9GPM,H9HD,H9HH,H9TD,"
outString +="H10,H10LVL,H10K,H10D,H10A,H10KDA,H10Gold,H10LH,H10DN,H10XPM,H10GPM,H10HD,H10HH,H10TD,"
outString +="SUM2LVL,SUM2K,SUM2D,SUM2A,SUM2KDA,SUM2Gold,SUM2LH,SUM2DN,SUM2XPM,SUM2GPM,SUM2HD,SUM2HH,SUM2TD"

outputFile.write(outString.encode("utf-8")+"\n".encode("utf-8"))	

#badFile = open('FAILCSV.csv', 'ab')

#Run for the alloted runs
totalRuns = 0
while totalRuns < runs:
	totalRuns += 1
	
	matchID = str(matchseed+totalRuns)
	print("MATCH:"+matchID)
	h1.request('GET',"/matches/"+matchID, headers=hdr)

	r1 = h1.getresponse()
	print(r1.status, r1.reason)
	
	if("Not Found" in r1.reason):
		h1.close()
		time.sleep(1)
		continue
	
	data = r1.read().decode()
	h1.close()

	#Begin parsing
	#All data stored in line 3, so get that line
	words = data.split("\n")
	words = words[2]
	#Feed it through our custom parser
	parser = MyHTMLParser()
	parser.feed(words)
	tagList = parser.returnResults()

	#Determine if our data is valid
	valid = checkValid(tagList)

	if valid == 1:
		print("VALID")
		#Get info of data in csv
		outString = ""
		tagList[0] = tagList[0][6:]
		tagList[1] = tagList[1][5:]
		tagList[3] = tagList[3][9:]
		tagList[4] = tagList[4][7:]
		tagList[5] = tagList[5][19:]
		
		for i in range(6,len(tagList)):
			if("STAT:" in tagList[i]):
				tagList[i] = tagList[i][5:]
				if("k" in tagList[i]):
					tagList[i] = tagList[i][:-1]
					tagList[i] = tagList[i] + "000"
					if("." in tagList[i]):
						tagList[i] = tagList[i][:-1]
						tagList[i] = tagList[i].replace(".", "")
			if("HERO:" in tagList[i]):
				tagList[i] = tagList[i][19:]
			if("SUM:" in tagList[i]):
				tagList[i] = tagList[i][4:]
				if("k" in tagList[i]):
					tagList[i] = tagList[i][:-1]
					tagList[i] = tagList[i] + "000"
					if("." in tagList[i]):
						tagList[i] = tagList[i][:-1]
						tagList[i] = tagList[i].replace(".", "")
		
		for item in tagList:
			outString += (item + ",")
		
		outString = outString[:-1]
		outputFile = open('SampleCSV.csv', 'ab')
		outputFile.write(outString.encode("utf-8")+"\n".encode("utf-8"))		
		outputFile.close()
	else:
		print("Bad elem")
		#Write the tags to the file that are relevant
		#for item in tagList:
		#	badFile.write(item.encode("utf-8")+"\n".encode("utf-8"))	

	#sleep so we're not a massive bully to dotabuff
	time.sleep(speed)
	

#badFile.close()