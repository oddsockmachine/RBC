
db: sudo docker-compose -f ./DB/docker-compose.yml up
elk: sudo docker-compose -f ./elk/docker-compose.yml up
collector: sleep 10 && cd ./collector && PYTHONUNBUFFERED=true ./venv/bin/python3 collector.py
cfg_mgr: sleep 10 && cd ./cfg_mgr && PYTHONUNBUFFERED=true ./venv/bin/python3 app.py
# mqtt: echo "todo!"
