import praw
import urllib2
import tweepy
import string
import math
from operator import attrgetter
from datetime import datetime
from pprint import pprint

class Source:
	plaintext = 0
	reddit = 1
	twitter = 2
	googleplus = 3
	ap = 4

class infoObj:
	author = ""
	title = ""
	link = ""
	thumbnail = ""
	body = ""
	source = Source.plaintext
	popularity = 0
	datepostedutc = ""
	algscore = 0
	#Add date created at source
	def __init__(self, titlein, linkin, sourcein):
		self.title = titlein
		self.link = linkin
		self.source = sourcein

def getRedditInfo(subin, amt):
	r = praw.Reddit(user_agent='Mikros Server Application: Providing submissions information for the latest interesting internet headlines')
	stack = []
	subreddit = r.get_subreddit(subin)

	for submission in subreddit.get_top_from_day(limit=amt):
		obj = infoObj(submission.title, submission.short_link, Source.reddit)
		obj.popularity = submission.ups
		obj.author = submission.author
		if submission.thumbnail != "self": 
			obj.thumbnail = submission.thumbnail
		else:
			body = submission.selftext
		stack.append(obj);

	return stack

def getTwitterInfo(userin, amt):
	CONSUMER_KEY = "Td1M6AcsRbwzGYKRb5484LZFd"
	CONSUMER_SECRET = "JVCH1ZgIAILiBAhoJLq9rGRYsVLaDz2ZOzebrBVEwsKdD2K9yp"
	stack = []
	auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	api = tweepy.API(auth);

	for status in tweepy.Cursor(api.user_timeline, id=userin, exclude_replies="true", include_rts="false").items(amt):
		obj = infoObj("", "https://twitter.com/statuses/"+str(status.id), Source.twitter)
		#for retweets: status.retweeted_status
		obj.body = status.text
		obj.thumbnail = status.user.profile_image_url
		obj.author = status.user.name
		obj.datepostedutc = status.created_at
		if status.retweeted == True:
			print("error")
		else:
			obj.popularity = status.retweet_count + status.favorite_count
		stack.append(obj)
	return stack

def sourceSort(sourcestack):
	univ = 100 #used for balancing the algorithm to be more readable
	for obj in sourcestack:
		if obj.source == Source.twitter:
			multiplier = 0.5
		else:
			multiplier = 1
		obj.algscore = (multiplier * math.sqrt(obj.popularity) * 3600 * univ)/getInfoAge(obj.datepostedutc, obj.source)
	return sorted(sourcestack, key=attrgetter("algscore"), reverse=True)

#Input is a string of the datetime in the UTC format
#Returns seconds ago a source was posted
def getInfoAge(inputa, sourcetype):
	return (datetime.utcnow() - inputa).total_seconds()

def main():
	#Examples:
	#test = getRedditInfo("futurology", 1)
	#print(test[0].popularity)
	sr = sourceSort(getTwitterInfo("elonmusk", 10))
	for x in range(0,10):
		print(sr[x].algscore)

if __name__ == "__main__":
	main()