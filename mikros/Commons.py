import time

class Source:
	plaintext = 0
	reddit = 1
	twitter = 2
	googleplus = 3
	newyorktimes = 4
	youtube = 5
	usatoday = 6

class Category:
	none = 0
	science = 1
	cooking = 2

class infoObj:
	author = ""
	#get Id based on title: Title is unique
	title = ""
	link = ""
	thumbnail = ""
	body = ""
	source = Source.plaintext
	popularity = 0
	datepostedutc = ""
	algscore = 0
	category = Category.none
	#Add date created at source
	def __init__(self, titlein, linkin, sourcein):
		self.title = titlein
		self.link = linkin
		self.source = sourcein

def SourceToString(obj):
	if obj is Source.reddit:
		return "reddit"
	elif obj is Source.twitter:
		return"twitter"
	elif obj is Source.googleplus:
		return "googleplus"
	elif obj is Source.newyorktimes:
		return "ap"
	elif obj is Source.plaintext:
		return"plaintext"
	elif obj is Source.youtube:
		return "youtube"
	elif obj is Source.usatoday:
		return "usatoday"
	else:
		return "plaintext"

def StringToSource(string):
	if string is "reddit":
		return Source.reddit
	elif string is "twitter":
		return Source.twitter
	elif string is "googleplus":
		return Source.googleplus
	elif string is "ap":
		return Source.ap
	elif string is "youtube":
		return Source.youtube
	elif string is "newyorktimes":
		return Source.newyorktimes
	elif string is "usatoday":
		return Source.usatoday
	else:
		return Source.plaintext

def getCategoryFromString(string):
	if string is "science":
		return Category.science
	elif string is "cooking":
		return Category.science
	else:
		return Category.none

def getAllCategories():
	a = Category()
	return [attr for attr in dir(a) if not attr.startswith("__")]	

if __name__ == "__main__":
	time.sleep(2)