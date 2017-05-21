from random import randint
from json import dumps

def report_temp(_id, client):
    print("Reporting temp")
    temp = randint(0,35)
    # global client
    client.publish("topic", "hello"+_id)
    client.publish("topic", dumps({'ID': _id, 'temp': temp}))
    # print(schedule.jobs)
    # print(schedule.next_run())
    return temp

def report_humidity(_id, client):
    print("Reporting hmdy")
    hmdy = randint(0,35)
    # global client
    client.publish("topic", "hello"+_id)
    client.publish("topic", dumps({'ID': _id, 'hmdy': hmdy}))
    # print(schedule.jobs)
    # print(schedule.next_run())
    return hmdy


def get_func(name):
    funcs = {
        "report_temp": report_temp,
        "report_humidity": report_humidity,
    }
    return funcs.get(name)
