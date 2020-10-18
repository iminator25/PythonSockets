import socket
import select
import errno
import sys

# setting constants here
HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 1234

# allow the user to have a username
my_username = input('Username: ')

# building the socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connecting the socket
client_socket.connect((IP,PORT))

# will allow us to handle errors
client_socket.setblocking(False)

# encode the username and username header
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')

# sending out the username to the server
client_socket.send(username_header + username)


while True:
	# building the message structure
	message = input(f"{my_username} > ")

	# if the message is not empty
	if message:
		# encode the message
		message = message.encode('utf-8')
		# build the message header
		message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
		# send the message
		client_socket.send(message_header + message)

	try:
		# find all the messages and receive them
		while True:
			# read in the headers for the received message
			username_header = client_socket.recv(HEADER_LENGTH)
			# if we recieved no data the connection was likley closed and we can leave
			if not len(username_header):
				print('connection closed by the server')
				sys.extit()

			# else receive the username
			username_length = int(username_header.decode('utf-8').strip())
			username = client_socket.recv(username_length).decode('utf-8')

			# then receive the message
			message_header = client_socket.recv(HEADER_LENGTH)
			message_length = int(message_header.decode('utf-8').strip())
			message = client_socket.recv(message_length).decode('utf-8')

			# nicely print the message
			print(f"{username} > {message}")

	except IOError as e:
		# This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
		if e.errno != errno.EAGAIN and e.errno != errno.EWOUDBLOCK:
			print('Reading error', str(e))
			sys.exit()
		# we just didnt receive anything
		continue



	except Exception as e:
		# any other exception, we can exit 
		print('General error', str(e))
		sys.exit()
	

