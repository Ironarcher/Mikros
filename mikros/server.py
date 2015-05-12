from socket import *
from thread import *
import pickle
import threading
import time
import apis
import os
import string
from . import *

import MySQLdb as mdb
import sys

class Source:
	plaintext = 0
	reddit = 1
	twitter = 2
	googleplus = 3
	ap = 4
	youtube = 5

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
	source = source.Source.plaintext
	popularity = 0
	datepostedutc = ""
	algscore = 0
	category = Category.none
	#Add date created at source
	def __init__(self, titlein, linkin, sourcein):
		self.title = titlein
		self.link = linkin
		self.source = sourcein

def pickleInfoObj(info):
	return pickle.dumps(info)

def receive(conn):
	packet = conn.recv(1024)
	if packet[0] == "0":
		#Type: Ping server for latency test. Return immediately
		reponse = "ping"
	elif packet[0] == "1":
		#Type: Use credentials to get followed categories
		packet.split("%s")
		if packet[1] is not None and packet[2] is not None:
			verify = getCredentials(packet[1], packet[2])
			if verify != "failure":
				response = getFollowedCategories(verify)
	elif packet[0] == "2":
		#Type: Use credentials to get best articles from selected category
		if packet[1] is not None and packet[2] is not None and packet[3] is not None:
			verify = getCredentials(packet[1], packet[2])
			if verify != "failure":
				response = ""
				data = getArticles(packet[3])
				for i in data:
					temp = pickleInfoObj(i) + "%s"
					response += temp
		response = ""
	elif packet[0] =="3":
		#Type: Use credentials to get list of sources from selected category
		#LATER (TO-DO)
		response = ""
	elif packet[0] == "4":
		#Type: Use credentials to rate a selected article based on ID
		#LATER (TO-DO)
		response = ""
	elif packet[0] == "5":
		'''
		Type: Create a new account by listing username, password, and email in that order
		by packet[1], [2], and [3]. "Success" is returned if account made and "useralreadyexists"
		is returned if the user already exists in the database
		'''
		packet.split("%s")
		if packet[1] is not None and packet[2] is not None and packet[3] is not None:
			response = createUser(packet[1], packet[2], packet[3])
	elif packet[0] == "6":
		#Type: LOGIN - Check in account credentials are valid and list login
		packet.split("%s")
		if packet[1] is not None and packet[2] is not None:
			response = getCredentials(packet[1], packet[2])
	elif packet[0] == "7":
		#Type: Use credentials to modify password (Require SSL maybe)
		response = ""
	elif packet[0] == "8":
		#Type: Use credentials to list an article as viewed
		response = ""
	elif packet[0] == "9":
		#Type: Use credentials to modify email address
		response = ""
	elif packet[0] == "10":
		#Add a new followed category
		response = ""
	else:
		response = ""
	conn.send(response)
	if response != "":
		print("Response successfully processed: " + response)
	else:
		print("Unknown packet header error")

def getCredentials(username, password):
	with con:
		cur = con.cursor()
		cur.execute("SELECT id FROM users WHERE user = %s AND password = %s", (username, password))
        row = cur.fetchone()
        if row is not None:
        	return row[0]
        	if not overloaded:
        		logUserActivity(row[0])
        else:
        	return "failure"

def logUserActivity(userid):
	with con:
		cur = con.cursor()
		cur.execute("UPDATE users SET last_login = CURDATE() WHERE id = %s", (userid))
		print("User Activity logged for number of rows: ", cur.rowcount)

def createUser(username, password, email):
	with con:
		cur = con.cursor()
		#A person cannot have the same username or email as someone else
		cur.execute("SELECT * FROM users WHERE user = %s",
			(username))
		row = cur.fetchone()
		if row is None:
			cur.execute("INSERT INTO users(user, password, email) VALUES (%s, %s, %s)",
				(username, password, email))
			cur.execute("SELECT id FROM users WHERE user = %s", (username))
			row2 = cur.fetchone()
			logUserActivity(row2[0])
			return "success"
		else:
			return "useralreadyexists"

#def updatePassword():

#def updateEmail():

def getFollowedCategories(userid):
	with con:
		cur = con.cursor()
		cur.execute("SELECT category FROM users WHERE id = %s", (userid))

def getArticles(categorytype):
	stack = []
	with con:
		cur = con.cursor()
		strused = "SELECT * FROM articles ORDER BY algscore LIMIT 10 WHERE category = %s"
		cur.execute(strused, (Commons.getCategoryFromString(categorytype)))
		rows = cur.fetchall()
		print("Fetched resulting articles for user")
		#Put into source class from the desc using 
		for row in rows:
			sourcetype = Commons.StringToSource(row[6])
			#Select source with 
			obj = Commons.infoObj(row[2], row[3], sourcetype)
			obj.author = row[1]
			obj.thumbnail = row[4]
			obj.body = row[5]
			obj.popularity = row[7]
			obj.datepostedutc = row[8]
			obj.algscore = row[9]
			obj.category = categorytype
			stack.append(obj)
	return stack

def addArticle(info):
	sourcetype = Commons.SourcetoString(info.source)
	with con:
		cur = con.cursor()
		cur.execute("SELECT COUNT(1) FROM articles WHERE title = %s", (info.title))
		if not cur.fetchone()[0]:
			#check limits here
			if(len(info.author) > 45):
				info.author = info.author[0:42] + "..."
			if(len(info.title) > 400):
				info.title = info.title[0:397] + "..."
			if(len(info.link) > 400):
				#TO-DO: Insert url shortener here
			if(len(info.thumbnail) > 500):
				#TO-DO: Insert url shortener here
			if(len(info.body) > 16,777,215):
				info.title = info.title[0:16,777,212] + "..."
			#Impossible to be bigger than BIGINT(20) and float (1.79E308 max) for popularity and algscore

			cur.execute("INSERT INTO articles(author, title, link, thumbnail, body, source, popularity, datepostedutc, algscore, category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
				(info.author, info.title, info.link, info.thumbnail, info.body, sourcetype, info.popularity, info.datepostedutc, info.algscore, info.category))
		else:
			cur.execute("UPDATE articles SET popularity = %s, algscore = %s WHERE title = %s",
				(info.popularity, info.algscore, info.title))
			print('set')

def getSourcesFromFile(filename):
	script_dir = os.path.dirname(__file__)
	rel_path = "sources\\" + filename + ".txt"
	abs_file_path = os.path.join(script_dir, rel_path)
	f = open(abs_file_path, "r")
	stack = []
	for line in f:
		stack.append(line)
	return stack

def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop(): # executed in another thread
                while not stopped.wait(interval): # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True # stop if the program exits
            function(*args, **kwargs)
            t.start()
            return stopped
        return wrapper
    return decorator

#Interval for 15 minutes: 900
@setInterval(900)
def updateTwitter():
	sources = getSourcesFromFile("twitter")
	for source in sources:
		print(source)
		for b in Commons.getAllCategories():
			if b in source:
				usedstr = string.replace(source, b + ": ", "")
				stack = apis.getTwitterInfo(usedstr, 10)
				for obj in stack:
					apis.setAlgScore(obj)
					obj.category = Commons.getCategoryFromString(b)
					addArticle(obj)
				break

#Interval for 30 minutes: 1800
@setInterval(10)
def updateReddit():
	print("updating")
	sources = getSourcesFromFile("reddit")
	for source in sources:
		print(source)
		for b in Commons.getAllCategories():
			if b in source:
				usedstr = string.replace(source, b + ": ", "")
				stack = apis.getRedditInfo(usedstr, 10)
				for obj in stack:
					apis.setAlgScore(obj)
					obj.category = Commons.getCategoryFromString(b)
					addArticle(obj)
				break
			
def main():
	#Initialize the database
	global con
	global overloaded
	overloaded = False
	con = mdb.connect('localhost', 'testuser2', 'test624', 'mikros2')
	with con:
		cur = con.cursor()
		cur.execute("SELECT VERSION()")
		ver = cur.fetchone()
		print "Database started"
		print "Database version : %s " % ver

	host = "localhost"
	port = 39172

	#print(createUser("test3", "standard", "arpad.kovesdy@gmail.com"))
	#print(getCredentials("test3", "standard")
	
	updateTwitter()
	updateReddit()
	print('done')

	s = socket()
	s.bind((host, port))
	s.listen(5)

	while True:
		conn, addr = s.accept()
		start_new_thread(receive, (conn,))

	conn.close()
	s.close()

if __name__ == "__main__":
	main()