mosquitto_pub -h 127.0.0.1 -t jobs/foo/add -m '{"name": "quick_temp", "function": "report_temp", "period": "5", "pin": "1"}'
