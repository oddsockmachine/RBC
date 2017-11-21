from datetime import datetime
from pony.orm import *
set_sql_debug(True)

db = Database()

class Nodule(db.Entity):
    id = PrimaryKey(int, auto=True)
    uid = Required(str, unique=True)
    name = Required(str)
    presence = Optional(bool)
    tags = Optional(str)
    created_at = Required(datetime)
    woken_at = Optional(datetime)
    power = Optional(float)
    lat = Optional(float)
    lon = Optional(float)
    sensors = Set('Sensor')
    location = Required('Location')


class Sensor(db.Entity):
    id = PrimaryKey(int, auto=True)
    uid = Required(str)
    name = Required(str)
    sensor_type = Required(str)
    pin = Required(str)
    period = Required(str)
    units = Required(str)
    remotenode = Required(Nodule)


class Location(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    url = Optional(str)
    description = Optional(str)
    remotenodes = Set(Nodule)
    children = Set('Location', reverse='parent')
    parent = Optional('Location', reverse='children')



class Link(db.Entity):
    id = PrimaryKey(int, auto=True)
    created_at = Required(str)
    url = Required(str)
    description = Required(str)





db.bind(provider='postgres', user='postgres', password='mysecretpassword', host='192.168.99.100', database='')
# db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)


with db_session:
    L1 = Link(created_at='Tuesday', url='facebook.com', description='Facebook')
    L2 = Link(created_at='Thursday', url='hackaday.com', description='HackADay')
