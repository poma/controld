#!/usr/bin/env python

import os, sys, time, socket, httplib2, datetime, thread, traceback
from daemon import Daemon
import settings

class MyDaemon(Daemon):
	def run(self):
		try:
			s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
			s.connect(settings.lircd_socket)
		except:
			self.log("Initialization exception, exiting!\n" + traceback.format_exc())
			raise
		while True:
			try:
				data = s.recv(1024)
			except:
				self.log("Data receive exception, exiting!\n" + traceback.format_exc())
				raise
			if not data:
				self.log("Socket closed, exiting")
				break
			self.log("Received: " + repr(data))
			key, count = self.parse(data)
			self.log("Parsed: %s, %s" % (key, count))
			thread.start_new_thread(self.process, (key, count))
		s.close()

	def log(self, message):
		open(settings.logfile, "a").write("[%s] %s\n" % (datetime.datetime.now(), message))
	
	def parse(self, line):
		a = line.split(' ')
		return (a[2], a[1])

	def process(self, key, count):
		try:
			if key in settings.keys_light:
				if (count != "00"): return
				for line in settings.keys_light[key]:
					command = settings.noolite_command + line
					self.log("Executing " + repr(command))
					code = os.system(command)
					self.log("Return code: " + repr(code))
					time.sleep(0.2)
			else:
				url = "http://%s/remote?key=%s&count=%s" % (settings.http_host, key, count)
				self.log("Requesting " + repr(url))
				r, content = httplib2.Http().request(url)
				self.log("Response code: %s %s; %s" % (r.status, r.reason, content))
				#if content != "ok":
				#self.log("Error on key %s: %s" % (repr(key), repr(content)))
		except:
			self.log("Error executing command, continuing execution!\n" + traceback.format_exc())
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
			print "usage: controld start|stop|restart|run"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: controld start|stop|restart|run"
		sys.exit(2)
