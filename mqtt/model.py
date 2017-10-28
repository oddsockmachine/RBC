import redis
import rom
from datetime import datetime
from conf import load_config
from uuid import uuid4
from json import dumps
config = load_config()
rom.util.set_connection_settings(host=config['REDIS_URL'], port=config['REDIS_PORT'])


class Location(rom.Model):
    name = rom.String(required=True, index=True, keygen=rom.FULL_TEXT)
    url = rom.String(required=True, index=True, unique=True, keygen=rom.FULL_TEXT)
    description = rom.String(required=True)
    parent = rom.ManyToOne('Location', on_delete='cascade')
    children = rom.OneToMany('Location', column='parent')
    # outline of grid coordinates for map
    def to_json(self):
        d = {}
        d['name'] = str(self.name.decode('utf-8'))
        d['url'] = str(self.url.decode('utf-8'))
        d['parent'] = {'name': self.parent.name.decode('utf-8'), 'url': self.parent.url.decode('utf-8')}
        d['children'] = [{'name':c.name.decode('utf-8'), 'url':c.url.decode('utf-8')} for c in self.children]
        return dumps(d)

class Sensor(rom.Model):
    name = rom.String(required=True, index=True, keygen=rom.FULL_TEXT)
    uid = rom.String(required=True, index=True, unique=True, keygen=rom.FULL_TEXT)
    # uid = "~".join([_self.name, sensor_type, job_name, pin])  # Tag so we can identify this function later.
    sensor_type = rom.String(required=True, index=True, keygen=rom.FULL_TEXT)  # What kind of sensor is this? eg DHT_11
    pin = rom.String()  # Pin identifier on chip, adc, i2c
    period = rom.Integer()  # In seconds
    units = rom.String()  # Human readable units
    node = rom.ManyToOne('Node', on_delete='cascade', required=True)

class Node(rom.Model):
    name = rom.String(required=True, index=True, keygen=rom.FULL_TEXT)
    uid = rom.String(required=True, index=True, unique=True, keygen=rom.FULL_TEXT)
    presence = rom.Boolean(default=False)  # Is it working, or has LastWill fired
    location = rom.ManyToOne('Location', required=True, on_delete='no action')  # human readable location
    # location_url = rom.String(required=True)  # TODO tree-based nested url eg farm/field1/greenhouse3/bed2
    tags = rom.String(index=True, keygen=rom.FULL_TEXT)
    # jobs = rom.Json()
    sensors = rom.OneToMany('Sensor')
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
        # self.jobs = {}
        # self.sensors = {}
        self.created_at = datetime.now()
        self.woken_at = datetime.now()
        self.presence = False
        self.power = 0.0
        return self

    def update_from_report(self, report):
        return

    def update_presence(self, presence):
        if presence.lower() == "connected":
            self.presence = True
        elif presence.lower() == "disconnected":
            self.presence = False
        self.save()

    def to_json(self):
        d = self.__dict__.get('_data')
        d['location'] = d['location'].url
        return d

def exists(uid):
    n = Node.query.filter(uid=uid).all()
    return (len(n) > 0)

def create_node(name, location_url, lat, lon, tags):
    uid = str(uuid4()).split("-")[0]
    location = get_location_by_url(location_url)
    n = Node(name=name, uid=uid, lat=lat, lon=lon, location=location, tags=tags).init()
    n.save()
    print(n)
    return n

def create_node_from_report(report):
    n = Node()
    # n.save()
    return n

def get_node_by_name(name):
    n = Node.query.filter(name=name).all()
    return n[0].to_json()

def get_node_by_id(uid):
    n = Node.query.filter(uid=uid).all()
    return n[0].to_json()

def get_all_nodes():
    n = Node.query.filter().all()
    return map(lambda x: x.to_json(), n)

def get_root_location():
    locs = Location.query.filter(name='root').all()
    if len(locs) == 1:
        print("Root location already established")
        return locs[0]
    elif len(locs) == 0:
        print("Creating new root location")
        root = Location(name='root', url='root', description='root node')
        root.save()
        return root
    else:
        raise("multiple root locations found!")

def create_location(name, description, parent):
    url = parent.url.decode('utf-8') + '/' + name.replace(' ', '_').lower()
    print(name, parent.name, parent.url, url)
    new_loc = Location(name=name, url=url, description='Our apartment', parent=parent)
    new_loc.save()
    return new_loc

def get_location_by_url(_url):
    locs = Location.query.filter(url=_url).all()
    # print(locs)
    if len(locs)==1:
        return locs[0]
    elif len(locs)==0:
        print("Location not found at url {}".format(_url))
        return None
    else:
        print("{} conflicting locations found at {}".format(len(locs), _url))
        return None

def get_graph_under_location(location):
    name = location.name if isinstance(location.name, str) else str(location.name.decode('utf-8'))
    graph = {'location': name, 'children': {}}
    for child in location.children:
        c_graph = get_graph_under_location(child)
        graph['children'][str(child.name.decode('utf-8'))] = c_graph
    return graph

root_location = get_root_location()

if __name__ == '__main__':
    # Node(name='bap', uid='265', lat=0.93, lon=1.15, location='place').init().save()

    # print(get_node_by_id('123').name)
    # print(get_node_by_name('bar').name)
    #
    # points = Node.query \
    #     .near('geo_index', 1.0, 1.0, 2500.0, 'mi', 2) \
    #     .limit(0, 50) \
    #     .all()
    # for p in points:
    #     print(p.name, p.lat, p.lon)

    # bayside = create_location('3 Bayside', 'Our apartment', root_location)
    # balcony = create_location('Balcony', 'On the balcony', bayside)
    # living_room = create_location('Living Room', 'In the living room', bayside)
    # print(root_location.children[0].children[0].name)
    # print(root_location.children[0].children[0].url)

    # print(get_location_by_url('root').children[0].name)
    # lroom = get_location_by_url('root/3_bayside/living_room')
    # window1 = create_location('East Window', 'Main window, East facing', lroom)
    # window2 = create_location('South Window', 'Main window, South facing', lroom)
    # window3 = create_location('West Window', 'Main window, West facing', lroom)
    # window4 = create_location('Kitchen Window', 'Kitchen window, West facing', lroom)
    # window5 = create_location('Desk Window', 'Desk window, East facing', lroom)

    from pprint import pprint
    graph = get_graph_under_location(root_location)
    pprint(graph)
