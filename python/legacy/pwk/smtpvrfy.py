import socket
import sys

if len(sys.argv) is not 2:
	print 'Usage: smtpvrfy.py <username>'
	sys.exit(0)

# create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to the server
connect = s.connect(('114.255.40.66', 25))
#receive the banner
banner = s.recv(1024)
print banner
# VRFY a user
s.send('VRFY ' + sys.argv[1] + '\r\n')
result = s.recv(1024)
print result
# close the socket
s.close()