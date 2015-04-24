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
	while True:
		conn.send("Test from server\n")
		data=conn.recv(1024)
		print(data)

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