import praw
import urllib2
from pprint import pprint

class Source:
	plaintext = 0
	reddit = 1
	twitter = 2
	googleplus = 3
	ap = 4

class infoObj:
	title = ""
	link = ""
	thumbnail = ""
	body = ""
	source = Source.plaintext;
	popularity = 0;
	#Add date created at source
	def __init__(self, titlein, linkin, sourcein):
		title = titlein
		link = linkin
		source = sourcein

def getRedditInfo(subin, amt):
	r = praw.Reddit(user_agent='Mikros Server Application: Providing submissions information for the latest interesting internet headlines')
	stack = []
	subreddit = r.get_subreddit(subin)
	for submission in subreddit.get_top_from_day(limit=amt):
		obj = infoObj(submission.title, submission.short_link, Source.reddit)
		obj.popularity = submission.ups
		if submission.thumbnail != "self": 
			obj.thumbnail = submission.thumbnail
		else:
			body = submission.selftext
		stack.append(obj);
	return stack;

def getTwitterInfo(userin):
	stack = []
	return stack;

def main():
	test = getRedditInfo("futurology", 1)
	print(test[0].popularity)

if __name__ == "__main__":
	main()