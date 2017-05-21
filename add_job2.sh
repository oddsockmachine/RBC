mosquitto_pub -h 127.0.0.1 -t jobs/foo/add -m '{"name": "blob", "function": "report_humidity", "period": "9"}'
