from socket import *
from thread import *
import pickle

import MySQLdb as mdb
import sys

class Source:
	plaintext = 0
	reddit = 1
	twitter = 2
	googleplus = 3
	ap = 4
	youtube = 5

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
		response = ""
	elif packet[0] =="3":
		#Type: Use credentials to get list of sources from selected category
		response = ""
	elif packet[0] == "4":
		#Type: Use credentials to rate a selected article based on ID
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
		cur.execute("SELECT * FROM users WHERE user = %s AND password = %s", (username, password))
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
			cur.execute("SELECT * FROM users WHERE user = %s", (username))
			row2 = cur.fetchone()
			logUserActivity(row2[0])
			return "success"
		else:
			return "useralreadyexists"

#def updatePassword():

#def updateEmail():

def getFollowedCategories(userid):
	return ""

def getArticles(limit):
	with con:
		cur = con.cursor()
		strused = "SELECT * FROM articles ORDER BY algscore LIMIT " + str(limit)
		cur.execute(strused)
		rows = cur.fetchall()
		print("Fetched resulting articles for user")
		#Put into source class from the desc using 
		for row in rows:
			#Select source with 
			obj = infoObj(row[2])
			
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

	print(createUser("test3", "standard", "arpad.kovesdy@gmail.com"))
	print(getCredentials("test3", "standard"))
	thread.sleep(10000)

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
