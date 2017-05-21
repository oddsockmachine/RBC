mosquitto_pub -h 127.0.0.1 -t jobs/foo/add -m '{"name": "blah", "function": "report_temp", "period": "5"}'
