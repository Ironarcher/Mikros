from socket import *
from thread import *

import MySQLdb as mdb
import sys

class Source:
	plaintext = 0
	reddit = 1
	twitter = 2
	googleplus = 3
	ap = 4
	youtube = 5

def receive(conn):
	packet = conn.recv(1024)
	if packet[0] == "0":
		#Type: Ping server for latency test. Return immediately
		reponse = "ping"
	elif packet[0] = "1":
		#Type: Use credentials to get followed categories
	elif packet[0] = "2":
		#Type: Use credentials to get best articles from selected category
	elif packet[0] = "3":
		#Type: Use credentials to get list of sources from selected category
	elif packet[0] = "4":
		#Type: Use credentials to rate a selected article based on ID
	elif packet[0] = "5":
		#Type: Create a new account by listing e-mail, username, and password
	elif packet[0] = "6":
		#Type: LOGIN - Check in account credentials are valid and list login
	elif packet[0] = "7":
		#Type: Use credentials to modify password (Require SSL maybe)
	elif packet[0] = "8":
		#Type: Use credentials to list an article as viewed
	else:
		response = ""
	conn.send(response)
	data=conn.recv(1024)
	print(data)

def getCredentials(packet):
	data = packet.split()
	username = data[1]
	password = data[2]
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM users WHERE username =  %s WHERE password = %s", 
        (username, password))
        	row = cur.fetchone()
	
def getArticles(limit):
	with con:
		cur = con.cursor()
		strused = "SELECT * FROM articles ORDER BY algscore LIMIT " + str(limit)
		cur.execute(strused)
		rows = cur.fetchall()
		desc = cur.description
		print("Fetched resulting articles for user")
		#Put into source class from the desc using 
		for row in rows:
			

def main():
	#Initialize the database
	global con
	con = mdb.connect('localhost', 'testuser', 'test623', 'mikros')
	with con:
		cur = con.cursor()
		cur.execute("SELECT VERSION()")
		ver = cur.fetchone()
		print "Database started"
		print "Database version : %s " % ver

	host = "localhost"
	port = 39172
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
