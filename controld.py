#!/usr/bin/env python
 
import sys, time, socket, httplib2, datetime
from daemon import Daemon

class MyDaemon(Daemon):
	lircd_address = '/var/run/lirc/lircd'
	noolite_command = 'noolite -api -'
	mac_host='192.168.0.101'
	logfile = '/var/log/controld'

	keys_light = {
		"KEY_1" : "sw_ch 5",
		"KEY_2" : "on_ch 5",
		"KEY_3" : "set_ch 5 50"
	}

	def run(self):
		s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		s.connect(lircd_address)
		while True:
			data = s.recv(1024)
			log('Received', repr(data))
			process(data)
		s.close()

	def log(self, message):
		open(logfile, "a").write("[%s] %s\n" % (datetime.datetime.now(), message))

	def process(self, key):
		if key in keys_light:
			os.system(noolite_command + keys_light[key])
		else
			r, content = httplib2.Http().request("http://" + mac_host + "/remote?key=" + key)
			if content != ok:
				log("Error on key %s: %s" % (key, content))








# Control daemon
if __name__ == "__main__":
	daemon = MyDaemon('/var/run/controld.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
