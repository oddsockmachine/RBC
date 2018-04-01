# from datetime import datetime
# from random import randint
# from json import dumps
#
# import socket
# def get_ip():
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     try:
#         # doesn't even have to be reachable
#         s.connect(('10.255.255.255', 1))
#         IP = s.getsockname()[0]
#     except:
#         IP = '127.0.0.1'
#     finally:
#         s.close()
#     return IP
#
#
# def default_data(node, args):
#     return{'job_ID': args.get('job_uid'),
#            'node': node.name,
#            'pin': args.get('pin'),
#            'timestamp': str(datetime.now())}
#
# def report_temp(client, args):
#     print("Reporting temp on pin "+args.get('pin'))
#     temp = randint(0,35)
#     node = client._userdata
#     response = default_data(node, args)
#     job_type = 'temp'
#     response.update({'type': job_type, 'units': 'C', 'value': temp})
#     channel = "topic/{}/{}/{}".format(node.name, job_type, args.get('job_uid'))
#     client.publish(channel, dumps(response))
#     return response
#
# def report_humidity(client, args):
#     print("Reporting hmdy on pin "+args.get('pin'))
#     hmdy = randint(0,35)
#     node = client._userdata
#     response = default_data(node, args)
#     job_type = 'hmdy'
#     response.update({'type': job_type, 'units': '%', 'value': hmdy})
#     channel = "topic/{}/{}/{}".format(node.name, job_type, args.get('job_uid'))
#     client.publish(channel, dumps(response))
#     return response
#
# def report_ip(client, args):
#     print("Reporting IP of nodule")
#     node = client._userdata
#     response = default_data(node, args)
#     job_type = 'IP'
#     ip_cfg = get_ip
#     response.update({'type': job_type, 'value': ip_cfg})
#     channel = "topic/{}/{}/{}".format(node.name, job_type, args.get('job_uid'))
#     client.publish(channel, dumps(response))
#     return response
#
#
# # def report_devices(client, args):
# #     print("Reporting IP of nodule")
# #     node = client._userdata
# #     response = default_data(node, args)
# #     job_type = 'IP'
# #     ip_cfg = get_ip
# #     response.update({'type': job_type, 'value': ip_cfg})
# #     channel = "topic/{}/{}/{}".format(node.name, job_type, args.get('job_uid'))
# #     client.publish(channel, dumps(response))
# #     return response
#
#
# # def reload_cfg(client, args):
# #     print("Reporting hmdy on pin "+args.get('pin'))
# #     hmdy = randint(0,35)
# #     node = client._userdata
# #     response = default_data(node, args)
# #     job_type = 'hmdy'
# #     response.update({'type': job_type, 'units': '%', 'value': hmdy})
# #     channel = "topic/{}/{}/{}".format(node.name, job_type, args.get('job_uid'))
# #     client.publish(channel, dumps(response))
# #     return response
# #
# # def pull_from_git(client, args):
# #     print("Reporting hmdy on pin "+args.get('pin'))
# #     hmdy = randint(0,35)
# #     node = client._userdata
# #     response = default_data(node, args)
# #     job_type = 'hmdy'
# #     response.update({'type': job_type, 'units': '%', 'value': hmdy})
# #     channel = "topic/{}/{}/{}".format(node.name, job_type, args.get('job_uid'))
# #     client.publish(channel, dumps(response))
# #     return response
#
#
#
#
# def get_func(name):
#     funcs = {
#         "report_temp": report_temp,
#         "report_humidity": report_humidity,
#         "report_ip": report_ip,
#     }
#     return funcs.get(name)
