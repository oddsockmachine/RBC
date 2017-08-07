from datetime import datetime
from random import randint
from json import dumps

def default_data(node, args):
    return{'job_ID': args.get('job_uid'),
           'node_ID': node.name,
           'pin': args.get('pin'),
           'timestamp': str(datetime.now())}

def report_temp(client, args):
    print("Reporting temp on pin "+args.get('pin'))
    temp = randint(0,35)
    node = client._userdata
    response = default_data(node, args)
    job_type = 'temp'
    response.update({'type': job_type, 'units': 'C', 'value': temp})
    channel = "topic/{}/{}/{}".format(node.name, job_type, args.get('job_uid'))
    client.publish(channel, dumps(response))
    return response

def report_humidity(client, args):
    print("Reporting hmdy on pin "+args.get('pin'))
    hmdy = randint(0,35)
    node = client._userdata
    response = default_data(node, args)
    job_type = 'hmdy'
    response.update({'type': job_type, 'units': '%', 'value': hmdy})
    channel = "topic/{}/{}/{}".format(node.name, job_type, args.get('job_uid'))
    client.publish(channel, dumps(response))
    return response


def get_func(name):
    funcs = {
        "report_temp": report_temp,
        "report_humidity": report_humidity,
    }
    return funcs.get(name)
