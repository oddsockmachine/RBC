from datetime import datetime, time
from pony.orm import *
from uuid import uuid4
# set_sql_debug(True)

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
    sensors = Set('Component')
    jobs = Set('Job')
    zone = Required('Zone')
    hw_type = Required(str)  # esp8266/esp32/raspi etc
    debug = Required(bool, default=True)  # Send everything to log
    err_log_size = Required(int, default=100)  # Number of errors to batch before publishing
    log_size = Required(int, default=100)  # Number of logs to batch before publishing
    topics = Required(Json, default=['sensors', 'logs', 'errors', 'report', 'presence'])  # List of topics to subscribe to
    batch = Required(bool, default=False)  # Batch up messages or stream?


class Component(db.Entity):
    id = PrimaryKey(int, auto=True)
    uid = Required(str, unique=True)
    name = Required(str)  # TODO needed?
    description = Required(str)  # What is this component doing, where is it placed?
    component_type = Required(str)  # eg DHT_11, ds18b20
    kind = Required(str)  # sensor or actuator - maybe unnecessary distinction
    pin = Required(str)  # Physical pin, i2c address etc
    nodule = Required('Nodule')
    jobs = Set('Job')  # actuators in particular may have multiple schedules


class Job(db.Entity):
    id = PrimaryKey(int, auto=True)
    uid = Required(str, unique=True)
    name = Required(str)
    description = Required(str)
    kind = Required(str)  # internal, sensor or actuator
    period = Optional(int)
    interval = Optional(int)
    units = Optional(str)
    at_time = Optional(time)
    start_day = Optional(str)
    tags = Required(str)
    component = Required('Component')
    params = Optional(Json)
    nodule = Required('Nodule')
    #   type: actuator
    # component_type = Required(str)




class Zone(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    url = Optional(str)
    description = Optional(str)
    nodules = Set(Nodule)
    children = Set('Zone', reverse='parent')
    parent = Optional('Zone', reverse='children')



class Link(db.Entity):
    id = PrimaryKey(int, auto=True)
    created_at = Required(str)
    url = Required(str)
    description = Required(str)





db.bind(provider='postgres', user='postgres', password='mysecretpassword', host='192.168.99.100', database='')
# db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

def uuid():
    """Generate a uid to identify components/jobs which is short enough to be human-usable"""
    uid = str(uuid4()).split('-')[0]
    return uid

if __name__ == '__main__':

    with db_session:
        # L1 = Link(created_at='Tuesday', url='facebook.com', description='Facebook')
        # L2 = Link(created_at='Thursday', url='hackaday.com', description='HackADay')
        # Z0 = Zone(name='root', url='/', description='root')
        # Z1 = Zone(name='3_bayside_village', url='/3_bayside_village', description='3 Bayside Village', parent=Z0)
        # Z2 = Zone(name='bedroom', url='/3_bayside_village/bedroom', description='Bedroom', parent=Z1)
        # Z3 = Zone(name='living_room', url='/3_bayside_village/living_room', description='Living Room', parent=Z1)
        # Z4 = Zone(name='balcony', url='/3_bayside_village/bedroom/balcony', description='Balcony', parent=Z2)
        # Z5 = Zone(name='counter', url='/3_bayside_village/living_room/counter', description='Counter Top', parent=Z3)
        # Z6 = Zone(name='window1', url='/3_bayside_village/living_room/window', description='Window by desk', parent=Z3)
        z_lr = Zone.get(name='living_room')
        print(z_lr.name)
        # Z7 = Zone(name='SE window', url='/3_bayside_village/living_room/se_window', description='South East Window', parent=Z3)
        # Z8 = Zone(name='SW window', url='/3_bayside_village/living_room/sw_window', description='South West Window', parent=Z3)

        # N1 = Nodule(uid='abc123', name='balcony', created_at=datetime.now(), zone=Z4, hw_type='esp8266')
        # N2 = Nodule(uid='def456', name='living room', created_at=datetime.now(), zone=Z3, hw_type='raspi')
        # N3 = Nodule(uid='ghi789', name='SE Window', created_at=datetime.now(), zone=Z7, hw_type='esp32')
        # N5 = Nodule(uid='jkl012', name='SW Window', created_at=datetime.now(), zone=Z8, hw_type='raspi')
        n_bal = Nodule.get(name='living room')
        print(n_bal.name)
        # c1 = Component(uid=uuid(), name='balc temp/hmdy', description='balcony temperature/humidity', kind='sensor', component_type='DHT_11', pin="1", nodule=N1)
        # c2 = Component(uid=uuid(), name='tom_soil_temp', description='tomato soil temp', kind='sensor', component_type='ds18b20', pin="i2c_2", nodule=N1)
        # c3 = Component(uid=uuid(), name='aub_soil_temp', description='aubergine soil temp', kind='sensor', component_type='ds18b20', pin="i2c_3", nodule=N1)
        # c4 = Component(uid=uuid(), name='tom_soil_moist', description='tomato soil moisture', kind='sensor', component_type='moisture', pin="4", nodule=N1)
        # c5 = Component(uid=uuid(), name='aub_soil_moist', description='aubergine soil moisture', kind='sensor', component_type='moisture', pin="5", nodule=N1)
        # c6 = Component(uid=uuid(), name='balc lux', description='balcony light intensity', kind='sensor', component_type='TSL2561', pin="i2c_6", nodule=N1)
        # c7 = Component(uid=uuid(), name='window', description='greenhouse window', kind='actuator', component_type='servo', pin="7", nodule=N1)
        # c8 = Component(uid=uuid(), name='pump', description='irrigation pump', kind='actuator', component_type='pump', pin="8", nodule=N1)

        #
        # j1 = Job(uid=uuid(), name='balcony air temp', description='Balcony air temperature and humidity', kind='sensor', interval='5', units='C/%', tags='_', component=c1, nodule=N1)
        # j2 = Job(uid=uuid(), name='tomato soil temp', description='Temperature of soil in tomato pot', kind='sensor', interval='20', units='C', tags='_', component=c2, nodule=N1)
        # j3 = Job(uid=uuid(), name='aubergine soil temp', description='Temperature of soil in aubergine pot', kind='sensor', interval='20', units='C', tags='_', component=c3, nodule=N1)
        # j4 = Job(uid=uuid(), name='tomato soil moisture', description='Moisture of soil in tomato pot', kind='sensor', interval='20', units='%', tags='_', component=c4, nodule=N1)
        # j5 = Job(uid=uuid(), name='aubergine soil moisture', description='Moisture of soil in aubergine pot', kind='sensor', interval='20', units='%', tags='_', component=c5, nodule=N1)
        # j6 = Job(uid=uuid(), name='balcony light', description='Light intensity on balcony', kind='sensor', interval='5', units='lux', tags='_', component=c6, nodule=N1)
        # j6 = Job(uid=uuid(), name='run pump', description='Runs the pump', kind='actuator', interval='25',  tags='_', component=c8, nodule=N1)

        # c9 = Component(uid=uuid(), name='chive_soil_moist', description='chive soil moisture', kind='sensor', component_type='moisture', pin="1", nodule=N2)
        # c10 = Component(uid=uuid(), name='room lux', description='living room light intensity', kind='sensor', component_type='TSL2561', pin="i2c_2", nodule=N2)
        # c11 = Component(uid=uuid(), name='lamp', description='thai lamp', kind='actuator', component_type='relay', pin="3", nodule=N2)
        c12 = Component(uid=uuid(), name='ds18b20', description='ds18b20', kind='sensor', component_type='ds18b20', pin="4", nodule=n_bal)

        # j7 = Job(uid=uuid(), name='chive_moist', description='Moisture of soil in chive pot', kind='sensor', interval='17',  tags='_', component=c9, nodule=N2)
        j8 = Job(uid=uuid(), name='ds18b20', description='ds18b20', kind='sensor', interval='10',  tags='_', component=c12, nodule=n_bal)
        # j8 = Job(uid=uuid(), name='room light', description='Light intensity in living rom', kind='sensor', interval='30',  tags='_', component=c10, nodule=N2)
        # j9 = Job(uid=uuid(), name='room lamp', description='Turns on lamp in living room', kind='actuator', interval='100',  tags='_', component=c11, nodule=N2)
