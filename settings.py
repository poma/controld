lircd_socket = '/var/run/lirc/lircd'
noolite_command = '/usr/local/bin/noolite -api -'
http_host = '172.16.128.4:5112'
logfile = '/var/log/controld'
pidfile = '/var/run/controld.pid'

keys_light = {
        "KEY_RED" : ["set_ch 5 100", "set_ch 6 100"],
        "KEY_GREEN" : ["set_ch 5 50", "set_ch 6 50"],
        "KEY_YELLOW" : ["set_ch 5 30", "set_ch 6 30"],
        "KEY_BLUE" : ["set_ch 5 20", "set_ch 6 20"],
        "KEY_TITLE" : ["sw_ch 5"],
        "KEY_TEXT" : ["sw_ch 6"],
        "KEY_CLEAR" : ["off_ch 5", "off_ch 6"]
        }
