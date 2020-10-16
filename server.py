import socket 
import time
import pickle




# fixed length header of HEADERSIZE
HEADERSIZE = 10


# Family type is AF_INET corresponding to IPV4
# Socket is SOCKET_STREAM corresponding to TCP
# this is a streaming socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# pretty much the localhost and then we have the 
# socket number that we are binding too. 
# socket is the endpoint that receives data. 
s.bind((socket.gethostname(), 1234))

# we want to listen to stuff, we will have a que of 5
s.listen(5)

while True:
	# anyone can connect, stroing the client object in client socket
	# storing the address or where they are coming from in address
	clientsocket, address = s.accept()
	print(f"Connection from {address} has been established!")

	d = {1: 'Hello', 2: 'SCOTT'}
	msg = pickle.dumps(d)


	# No matter what you will get the message sent to the client
	# msg = 'Welcome to the server!'
	msg = bytes(f'{len(msg):<{HEADERSIZE}}', 'utf-8') + msg
	clientsocket.send(msg)

	# while True:
	# 	time.sleep(2)
	# 	msg = f"NO NO NO the time is {time.time()}"
	# 	msg = f'{len(msg):<{HEADERSIZE}}' + msg
	# 	clientsocket.send(bytes(msg, 'utf-8'))

	