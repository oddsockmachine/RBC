import redis
import rom
from datetime import datetime
from conf import load_config
config = load_config()

rom.util.set_connection_settings(host=config['REDIS_URL'], port=config['REDIS_PORT'])



class Node(rom.Model):
    name = rom.String(required=True, index=True, keygen=rom.FULL_TEXT)
    uid = rom.String(required=True, index=True, unique=True, keygen=rom.FULL_TEXT)
    presence = rom.Boolean(default=False)  # Is it working, or has LastWill fired
    location = rom.String(required=True)  # human readable location
    tags = rom.String(index=True, keygen=rom.FULL_TEXT)
    jobs = rom.Json()
    sensors = rom.Json()
    created_at = rom.DateTime()  # When was this node first activated
    woken_at = rom.DateTime()  # When did this node last wake up
    power = rom.Float()  # Battery power remaining
    lon = rom.Float()
    lat = rom.Float()
    def geo_cb(data):
        return data

    geo_index = [
        # callback function passed to GeoIndex as the 2nd argument *must*
        # return a dictionary containing 'lon' and 'lat' values, as degrees
        rom.GeoIndex('geo_index', geo_cb),
        ]

    def init(self):
        self.jobs = {}
        self.sensors = {}
        self.created_at = datetime.now()
        self.woken_at = datetime.now()
        return self

    def update_with_report(self, report):
        return

    def update_presence(self, presence):
        if presence.lower() == "connected":
            self.presence = True
        elif presence.lower() == "disconnected":
            self.presence = False
        self.save()


def get_node_by_name(name):
    n = Node.query.filter(name=name).all()
    return n[0]

def get_node_by_id(uid):
    n = Node.query.filter(uid=uid).all()
    return n[0]

# n1 = Node(name='foo', uid='123', lat=1.1, lon=0.9, location='place').init().save()
# n2 = Node(name='bar', uid='456', lat=0.9, lon=1.1, location='place').init().save()
# Node(name='bap', uid='265', lat=0.93, lon=1.15, location='place').init().save()
# Node(name='baz', uid='364', lat=0.95, lon=1.11, location='place').init().save()
# Node(name='fuz', uid='342', lat=0.91, lon=1.13, location='place').init().save()
# Node(name='bip', uid='234', lat=0.92, lon=1.19, location='place').init().save()

# print(get_node_by_id('123').name)
# print(get_node_by_id('123').jobs)
# print(get_node_by_id('123').presence)
# print(get_node_by_name('bar').name)
# print(get_node_by_name('bar').jobs)
# print(get_node_by_name('bar').presence)
#

points = Node.query \
    .near('geo_index', 1.0, 1.0, 2500.0, 'mi', 2) \
    .limit(0, 50) \
    .all()
for p in points:
    print(p.name, p.lat, p.lon)
