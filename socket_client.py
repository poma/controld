#!/usr/bin/env python
import socket

server_address = '/var/run/lirc/lircd'

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(server_address)
while 1:
	data = s.recv(1024)
	print 'Received', repr(data)
s.close()