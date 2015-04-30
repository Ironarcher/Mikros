import praw
import urllib2
import tweepy
import string
import math
import urllib2
import json
import xmltodict
from apiclient.discovery import build
from apiclient.errors import HttpError
from operator import attrgetter
from datetime import datetime
from pprint import pprint

class Source:
	plaintext = 0
	reddit = 1
	twitter = 2
	googleplus = 3
	ap = 4
	youtube = 5
	usatoday = 6

class Category:
	none = 0
	science = 1
	cooking = 2

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
	infoid = 0
	category = Category.none
	#Add date created at source
	def __init__(self, titlein, linkin, sourcein):
		self.title = titlein
		self.link = linkin
		self.source = sourcein

def getUsaTodayInfo(amt):
	apikey = "87r3b9p8z8xmpyhefhsfar4v"
	url = "http://api.usatoday.com/open/articles/topnews/tech?api_key=" + apikey
	contents = urllib2.urlopen(url)
	data = xmltodict.parse(contents)
	for articles in data['channel']['item']:
		pass
		
def getNytimesInfo(amt):
	apikey = "869383e665d02b1daedba543139595fb:19:71871736"
	pass

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
		obj = infoObj(status.text, "https://twitter.com/statuses/"+str(status.id), Source.twitter)
		#for retweets: status.retweeted_status
		#Omit infoObj body
		obj.thumbnail = status.user.profile_image_url
		obj.author = status.user.name
		obj.datepostedutc = status.created_at
		if status.retweeted == True:
			print("error")
		else:
			obj.popularity = status.retweet_count + status.favorite_count
		stack.append(obj)
	return stack

#Note: input category must be lowercase and must be one youtube's accepted categories
def getVideo_Playlist(playlist_id, amt):
	youtube = build("youtube", "v3", developerKey="AIzaSyDUrP5kVynFcdUozz6Et9BFZjpRFlMNYF0")
	videostack = []
	uniquevid_ids = []
	playlistitems_list_request = youtube.playlistItems().list(
		#maxResults=amt,
		playlistId=playlist_id,
    	part="snippet",
	)
	print(amt)
	#while playlistitems_list_request:
	playlistitems_list_response = playlistitems_list_request.execute()
	for playlist_item in playlistitems_list_response["items"]:
   		vid = infoObj(playlist_item["snippet"]["title"],
    	"https://www.youtube.com/watch?v=" + playlist_item["snippet"]["resourceId"]["videoId"],
    	Source.youtube)
    	vid.ident = playlist_item["snippet"]["resourceId"]["videoId"]
    	vid.author = playlist_item["snippet"]["channelTitle"]
    	videostack.append(vid)
    	uniquevid_ids.append(playlist_item["snippet"]["resourceId"]["videoId"])
    	print(len(playlist_item))
		#playlistitems_list_request = youtube.playlistItems().list_next(playlistitems_list_request, playlistitems_list_response)
	print('here')
	video_response = youtube.videos().list(
    	id=uniquevid_ids,
    	part='snippet, statistics'
	).execute()
	for vid_item, i in enumerate(video_response.get("items", [])):
		videostack[i].datepostedutc = vid_item["snippet"]["publishedAt"]
		videostack[i].thumbnail = vid_item[i]["snippet"]["thumbnails"]["standard"]["url"]
		videostack[i].popularity = vid_item[i]["statistics"]["viewcount"]

	return videostack

def getVideos_user(username, amt):
	youtube = build("youtube", "v3", developerKey="AIzaSyDUrP5kVynFcdUozz6Et9BFZjpRFlMNYF0")
	search_response = youtube.channels().list(
		forUsername=username,
		part="contentDetails",
	).execute()
	search_result = search_response.get("items", [])
	uploads_playlist_id = search_result[0]["contentDetails"]["relatedPlaylists"]["uploads"]
	return getVideo_Playlist(uploads_playlist_id, amt)

def getVideos_id(userid, amt):
	youtube = build("youtube", "v3", developerKey="AIzaSyDUrP5kVynFcdUozz6Et9BFZjpRFlMNYF0")
	search_response = youtube.channels().list(
		id=userid,
		part="contentDetails",
	).execute()
	search_result = search_response.get("items", [])
	uploads_playlist_id = search_result[0]["contentDetails"]["relatedPlaylists"]["uploads"]
	return getVideo_Playlist(uploads_playlist_id, amt)

def sourceSort(sourcestack):
	univ = 100 #used for balancing the algorithm to be more readable
	for obj in sourcestack:
		if obj.source == Source.twitter:
			multiplier = 0.5
		else:
			multiplier = 1
		obj.algscore = (multiplier * math.sqrt(obj.popularity) * 3600 * univ)/getInfoAge(obj.datepostedutc, obj.source)
	return sorted(sourcestack, key=attrgetter("algscore"), reverse=True)

def setAlgScore(obj):
	if obj.datepostedutc is not None and obj.popularity is not None:
		univ = 100
		if obj.source == Source.twitter:
			multiplier = 0.5
		else:
			multiplier = 1
		obj.algscore = (multiplier * math.sqrt(obj.popularity) * 3600 * univ)/getInfoAge(obj.datepostedutc, obj.source)

#Input is a string of the datetime in the UTC format
#Returns seconds ago a source was posted
def getInfoAge(inputa, sourcetype):
	return (datetime.utcnow() - inputa).total_seconds()

def main():
	#Examples:
	#test = getRedditInfo("futurology", 1)
	#print(test[0].popularity)
	#sr = sourceSort(getTwitterInfo("elonmusk", 10))
	#for x in range(0,10):
	#	print(sr[x].algscore)
	videos = getVideos_user("CarbotAnimations", "25")
	print(videos[0].datepostedutc)
	print(videos[1].title)
	print(videos[2].title)
	print(videos[3].title)
	#print(videos[1].title)

if __name__ == "__main__":
	main()