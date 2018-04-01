from flask import Flask

import peewee

import flask_admin as admin
from flask_admin.contrib.peewee import ModelView
from playhouse.postgres_ext import JSONField


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456790'

# db = peewee.SqliteDatabase('test.sqlite', check_same_thread=False)

db = peewee.PostgresqlDatabase('postgres', user='postgres', password='mysecretpassword',
                           host='dmip', port=5432)

class BaseModel(peewee.Model):
    class Meta:
        database = db


class User(BaseModel):
    username = peewee.CharField(max_length=80)
    email = peewee.CharField(max_length=120)

    def __unicode__(self):
        return self.username


class Post(BaseModel):
    # title = peewee.CharField(max_length=120)
    text = peewee.TextField(null=False)
    date = peewee.DateTimeField()

    user = peewee.ForeignKeyField(User)

    def __unicode__(self):
        return self.title


class UserAdmin(ModelView):
    pass

class PostAdmin(ModelView):
    pass
    # Visible columns in the list view
    # column_exclude_list = ['text']
    #
    # # List of columns that can be sorted. For 'user' column, use User.email as
    # # a column.
    # column_sortable_list = ('title', ('user', User.email), 'date')
    #
    # # Full text search
    # column_searchable_list = ('title', User.username)
    #
    # # Column filters
    # column_filters = ('title',
    #                   'date',
    #                   User.username)
    #
    # form_ajax_refs = {
    #     'user': {
    #         'fields': (User.username, 'email')
    #     }
    # }









class Zone(BaseModel):
    name = peewee.CharField(max_length=80)
    url = peewee.CharField(max_length=80)
    description = peewee.CharField(max_length=80)
    # parent = peewee.ForeignKeyField('self', null=True, backref='children')


class Nodule(BaseModel):
    # uid = peewee.CharField(max_length=80)
    name = peewee.CharField(max_length=80)
    presence = peewee.BooleanField()
    tags = peewee.CharField(max_length=80)
    created_at = peewee.DateTimeField()
    woken_at = peewee.DateTimeField()
    power = peewee.FloatField()
    lat = peewee.FloatField()
    lon = peewee.FloatField()
    zone = peewee.ForeignKeyField(Zone)
    hw_type = peewee.CharField(max_length=80)  # esp8266/esp32/raspi etc
    debug = peewee.BooleanField()
    err_log_size = peewee.IntegerField()
    log_size = peewee.IntegerField()
    topics = JSONField(default=['sensors', 'logs', 'errors', 'report', 'presence'])  # List of topics to subscribe to
    batch = peewee.BooleanField()


class Component(BaseModel):
    # uid = peewee.CharField(max_length=80)
    name = peewee.CharField(max_length=80)  # TODO needed?
    description = peewee.CharField(max_length=80)  # What is this component doing, where is it placed?
    component_type = peewee.CharField(max_length=80)  # eg DHT_11, ds18b20
    kind = peewee.CharField(max_length=80)  # sensor or actuator - maybe unnecessary distinction
    pin = peewee.CharField(max_length=80)  # Physical pin, i2c address etc
    nodule = peewee.ForeignKeyField(Nodule)


class Job(BaseModel):
    # uid = peewee.CharField(max_length=80)
    name = peewee.CharField(max_length=80)
    description = peewee.CharField(max_length=80)
    kind = peewee.CharField(max_length=80)  # internal, sensor or actuator
    period = peewee.IntegerField()
    interval = peewee.IntegerField()
    units = peewee.CharField(max_length=80)
    at_time = peewee.TimeField()
    start_day = peewee.CharField(max_length=80)
    tags = peewee.CharField(max_length=80)
    component = peewee.ForeignKeyField(Component)
    params = JSONField()
    nodule = peewee.ForeignKeyField(Nodule)
    #   type: actuator
    # component_type = peewee.CharField(max_length=80)


# todo: convert cfg_mgrs models to use peewee or sqla


class UserAdmin(ModelView):
    pass

class ZoneAdmin(ModelView):
    pass
class NoduleAdmin(ModelView):
    pass
class ComponentAdmin(ModelView):
    pass
class JobAdmin(ModelView):
    pass









@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


if __name__ == '__main__':
    import logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    admin = admin.Admin(app, name='Example: Peewee')

    admin.add_view(UserAdmin(User))
    admin.add_view(PostAdmin(Post))
    admin.add_view(ZoneAdmin(Zone))
    admin.add_view(NoduleAdmin(Nodule))
    admin.add_view(ComponentAdmin(Component))
    admin.add_view(JobAdmin(Job))

    try:
        User.create_table()
        # UserInfo.create_table()
        Post.create_table()
    except:
        pass

    app.run(debug=True)
