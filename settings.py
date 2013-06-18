lircd_socket = '/var/run/lirc/lircd'
noolite_command = '/usr/local/bin/noolite -api -'
http_host = '172.16.128.2:8080'
logfile = '/var/log/controld'
pidfile = '/var/run/controld.pid'

keys_light = {
	"KEY_RED" : ["sw_ch 5", "sw_ch 6", "sw_ch 7"],
	"KEY_GREEN" : ["sw_ch 6"],
	"KEY_YELLOW" : ["sw_ch 5"],
	"KEY_BLUE" : ["sw_ch 7"],
	"KEY_TITLE" : ["set_ch 5 50", "set_ch 6 50"],
	"KEY_TEXT" : ["set_ch 5 100", "set_ch 6 100"],
	"KEY_CLEAR" : ["off_ch 5", "off_ch 6", "off_ch 7"]
	}
