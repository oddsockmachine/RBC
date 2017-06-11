mosquitto_pub -h 127.0.0.1 -t jobs/foo/add -m '{"name": "slow_hmdty", "function": "report_humidity", "period": "10", "pin": "2"}'
