#!/usr/bin/env python
 
import os, sys, time, socket, httplib2, datetime, thread
from daemon import Daemon

class MyDaemon(Daemon):
	lircd_address = '/var/run/lirc/lircd'
	noolite_command = 'noolite -api -'
	mac_host = '192.168.0.101'
	logfile = '/var/log/controld'

	keys_light = {
		"KEY_1" : "sw_ch 6",
		"KEY_2" : "on_ch 6",
		"KEY_3" : "set_ch 6 50"
	}

	def run(self):
		s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		s.connect(self.lircd_address)
		while True:
			data = s.recv(1024)
			if not data: 
				self.log("Socket closed, exiting")
				break
			self.log("Received: " + repr(data))
			thread.start_new_thread(self.process, data.strip())
		s.close()

	def log(self, message):
		open(self.logfile, "a").write("[%s] %s\n" % (datetime.datetime.now(), message))

	def process(self, key):
		if key in self.keys_light:
			command = self.noolite_command + self.keys_light[key]
			self.log("Executing " + repr(command))
			code = os.system(command)
			self.log("Return code: " + repr(code))
		else:
			url = "http://%s/remote?key=%s" % (self.mac_host, key)
			self.log("Requesting " + repr(url))
			r, content = httplib2.Http().request(url)
			self.log("Response code: %s %s" % (r.status, r.reason))
			#if content != "ok":
			#	self.log("Error on key %s: %s" % (repr(key), repr(content)))






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
                elif 'run' == sys.argv[1]:
                        daemon.run()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
