#!/usr/bin/env python

import os, sys, time, socket, httplib2, datetime, thread, traceback
from daemon import Daemon
import settings

class MyDaemon(Daemon):
	def run(self):
		try:
			s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
			s.connect(settings.lircd_address)
		except:
			self.log("Initialization exception!\n" + traceback.format_exc())
			raise
		while True:
			try:
				data = s.recv(1024)
			except:
				self.log("Data receive exception!\n" + traceback.format_exc())
				raise
			if not data:
				self.log("Socket closed, exiting")
				break
			self.log("Received: " + repr(data))
			thread.start_new_thread(self.process, (data.strip(), ))
		s.close()

	def log(self, message):
		open(settings.logfile, "a").write("[%s] %s\n" % (datetime.datetime.now(), message))

	def process(self, key):
		try:
			if key in settings.keys_light:
				command = settings.noolite_command + settings.keys_light[key]
				self.log("Executing " + repr(command))
				code = os.system(command)
				self.log("Return code: " + repr(code))
			else:
				url = "http://%s/remote?key=%s" % (settings.mac_host, key)
				self.log("Requesting " + repr(url))
				r, content = httplib2.Http().request(url)
				self.log("Response code: %s %s" % (r.status, r.reason))
				#if content != "ok":
				#self.log("Error on key %s: %s" % (repr(key), repr(content)))
		except:
			self.log("Error executing command!\n" + traceback.format_exc())
			#raise






# Control daemon
if __name__ == "__main__":
	daemon = MyDaemon(settings.pidfile)
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
