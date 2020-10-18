# socket is good for making sockets lol
# select allows OS level I/O capabilities which allows sockets to work 
# the same over different OS's 

import socket
import select

HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 1234

# Creating the socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# setting the port so that we dont have to change the number each time.
# pretty much allows the port to be used multiple times or resets it

server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

# binding the socket 
server_socket.bind((IP, PORT))

# listening to clients 
server_socket.listen()

# list of conenctied sockets, good to have for OS level instructions
sockets_list = [server_socket]

# dict for coneected clients - key = socket, value = username
clients = {}


# function for handling incoming messages
def receive_message(client_socket):
	try:
		# reads in the header which tells us how long the message is
		message_header = client_socket.recv(HEADER_LENGTH)

		# if we recieved no data, the client closed thier socket 
		if not len(message_header):
			return False

		# else we got data and we read the lenght of the data 
		# and we return the message 
		message_length = int(message_header.decode('utf-8').strip())
		return {'header': message_header, 'data': client_socket.recv(message_length)}

	except:
		# we are here if the client closes thier connection violently
		return False


while True:
	 # Calls Unix select() system call or Windows select() WinSock call with three parameters:
    #   - rlist - sockets to be monitored for incoming data
    #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
    #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
    # Returns lists:
    #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
    #   - writing - sockets ready for data to be send thru them
    #   - errors  - sockets with some exceptions
    # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
	read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

	# loops over read sockets 
	for notified_socket in read_sockets:
		# if its a server socket its a new connection and we can accept it
		if notified_socket == server_socket:
			client_socket, client_address = server_socket.accept()

			# read in the message 
			user = receive_message(client_socket)

			# client disconected before they sent his name
			if user is False:
				continue
			# upadate socket list to add the new connection
			sockets_list.append(client_socket)
			clients[client_socket] = user

			print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")

		# an existing socket is sending a message
		else:
			# recieve the message
			message = receive_message(notified_socket)

			# reached if the cient disconnected so we need to get rid of them
			if message is False:
				print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
				sockets_list.remove(notified_socket)
				del clients[notified_socket]
				continue

			# gets user from notified socket and we can print the data
			user = clients[notified_socket]
			print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")


			# send out message to all other people
			for client_socket in clients:
				if client_socket != notified_socket:
					# send out the user data and headers as we did previously 
					client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

	# hanling possible errors. 
	for notified_socket in exception_sockets:
		sockets_list.remove(notified_socket)
		del clients[notified_socket]
