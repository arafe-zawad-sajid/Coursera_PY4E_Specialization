# 12.1 - Networked Tehcnology

# STEP 1: make a conection to a port
import socket as skt  # importing the socket library

# create a socket: ready to connect, doorway created
mysock = skt.socket(skt.AF_INET, skt.SOCK_STREAM)  # like file handle
# actual connection: just dialing the phone (web server)
mysock.connect(('data.pr4e.org', 80))  # single tuple as paramter
# ---------

# 12.2 - HTTP

# STEP 2: send a GET request
# prepare a request for sending: make up a request as a string and encode() it
cmd = 'GET http://data.pr4e.org/romeo.txt HTTP/1.0\r\n\r\n'.encode()  # encode(): unicode to utf8
# cmd = 'GET http://data.pr4e.org/intro-short.txt HTTP/1.0\r\n\r\n'.encode()

# send the GET request
mysock.send(cmd)  # like file handle

# STEP 3: get some data back
# receiving data sent back from the server
while True:
    data = mysock.recv(512)  # receive upto 512 chars
    if len(data) < 1:  # no data / EOF
        break
    print(data.decode(), end='')  # decode() received data: utf8 to unicode

# close the connection (socket)
mysock.close()
