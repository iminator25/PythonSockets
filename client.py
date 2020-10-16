import socket
import pickle
HEADERSIZE = 10


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# clients want to connect while servers want to bind
# we will connect here making the connection to the right port
s.connect((socket.gethostname(), 1234))

# choosing the size of the chunks of data we want to recieve
# at a time, dependant on application etc. 
#	msg = s.recv(1024)
while True:
	full_msg = b''
	new_msg = True

	while True:
		msg = s.recv(16)
		if new_msg:
			print(f'new message length: {msg[:HEADERSIZE]}')
			msglen = int(msg[:HEADERSIZE])
			new_msg = False


		full_msg += msg
		# print('breaks\n'+ full_msg)

		if len(full_msg) - HEADERSIZE == msglen:
			print('full msg received')
			print(full_msg[HEADERSIZE:])

			d = pickle.loads(full_msg[HEADERSIZE:])
			print(d)
			
			new_msg = True
			full_msg = b''

# print(full_msg)


