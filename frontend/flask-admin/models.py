from peewee import *
from playhouse.postgres_ext import *
from os import environ

host = environ.get("db_host", "192.168.99.100")
pw = environ.get("db_pw", "mysecretpassword")

database = PostgresqlDatabase('postgres', **{'host': host, 'user': 'postgres', 'password': pw})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Zone(BaseModel):
    description = TextField()
    name = TextField()
    parent = ForeignKeyField(column_name='parent', field='id', model='self', null=True)
    url = TextField()

    class Meta:
        table_name = 'zone'

class Nodule(BaseModel):
    batch = BooleanField()
    created_at = DateTimeField()
    debug = BooleanField()
    err_log_size = IntegerField()
    hw_type = TextField()
    lat = FloatField(null=True)
    log_size = IntegerField()
    lon = FloatField(null=True)
    name = TextField()
    power = FloatField(null=True)
    presence = BooleanField(null=True)
    tags = TextField()
    topics = BinaryJSONField()
    uid = TextField(unique=True)
    woken_at = DateTimeField(null=True)
    zone = ForeignKeyField(column_name='zone', field='id', model=Zone)

    class Meta:
        table_name = 'nodule'

class Component(BaseModel):
    component_type = TextField()
    description = TextField()
    kind = TextField()
    name = TextField()
    nodule = ForeignKeyField(column_name='nodule', field='id', model=Nodule)
    pin = TextField()
    uid = TextField(unique=True)

    class Meta:
        table_name = 'component'

class Job(BaseModel):
    at_time = TimeField(null=True)
    component = ForeignKeyField(column_name='component', field='id', model=Component)
    description = TextField()
    interval = IntegerField(null=True)
    kind = TextField()
    name = TextField()
    nodule = ForeignKeyField(column_name='nodule', field='id', model=Nodule)
    params = BinaryJSONField(null=True)
    period = IntegerField(null=True)
    start_day = TextField()
    tags = TextField()
    uid = TextField(unique=True)
    units = TextField()

    class Meta:
        table_name = 'job'

class Link(BaseModel):
    created_at = TextField()
    description = TextField()
    url = TextField()

    class Meta:
        table_name = 'link'

class User(BaseModel):
    email = CharField()
    username = CharField()

    class Meta:
        table_name = 'user'

class Post(BaseModel):
    date = DateTimeField()
    text = TextField()
    user = ForeignKeyField(column_name='user_id', field='id', model=User)

    class Meta:
        table_name = 'post'
