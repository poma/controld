#!/usr/bin/env python
import socket, os, time

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
	os.remove("/var/run/lirc/lircd")
except OSError:
	pass
s.bind("/var/run/lirc/lircd")
s.listen(1)
conn, addr = s.accept()
conn.send("KEY_1\n")
time.sleep(1)
conn.send("KEY_MUTE\n")
conn.close()