mosquitto_pub -h 127.0.0.1 -t jobs/bar/add -m '{"name": "slow_mock", "sensor_type": "Mock", "period": "6", "pin": "2"}'
