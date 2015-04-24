from socket import *


def main():
	host = "localhost"
	port = 39172
	s = socket()
	s.connect((host, port))

	data = s.recv(1024)
	print(data)
	s.send("Hello, from client.")

	s.close()

if __name__ == "__main__":
	main()