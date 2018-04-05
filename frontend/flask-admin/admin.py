from flask import Flask

import peewee

import flask_admin as admin
from flask_admin.contrib.peewee import ModelView

from models import *
from redis import Redis
from flask_admin.contrib import rediscli

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456790'

# db = peewee.SqliteDatabase('test.sqlite', check_same_thread=False)

# db = peewee.PostgresqlDatabase('postgres', user='postgres', password='mysecretpassword',
                           # host='dmip', port=5432)

class BaseModel(peewee.Model):
    class Meta:
        database = database


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



class OverView(ModelView):
    create_modal = True
    edit_modal = True
    page_size = 50
    column_sortable_list = ()
    can_set_page_size = True

    pass

class ZoneAdmin(OverView):
    column_list = ['name', 'description', 'parent', ]
    pass

class NoduleAdmin(OverView):
    column_list = ['name', 'uid', 'zone', 'hw_type', 'presence', 'debug', 'power', 'tags',  'batch', ]
    column_descriptions = dict(
        name='First and Last name'
    )
    pass

class ComponentAdmin(OverView):
    column_list = ['name', 'description', 'component_type', 'kind', 'pin', 'nodule', ]
    form_choices = {
    'kind': [
        ('sensor', 'sensor'),
        ('actuator', 'actuator')
        ]
    }
    pass

class JobAdmin(OverView):
    column_list = ['name', 'description', 'kind', 'units', 'interval', 'period', 'at_time', 'start_day', 'nodule',  'params', 'tags',]
    pass









@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


if __name__ == '__main__':
    import logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    admin = admin.Admin(app, name='RBC Admin', template_mode='bootstrap3')

    admin.add_view(UserAdmin(User))
    admin.add_view(PostAdmin(Post))
    admin.add_view(ZoneAdmin(Zone))
    admin.add_view(NoduleAdmin(Nodule))
    admin.add_view(ComponentAdmin(Component))
    admin.add_view(JobAdmin(Job))
    admin.add_view(rediscli.RedisCli(Redis(host="dmip")))

    try:
        User.create_table()
        # UserInfo.create_table()
        Post.create_table()
    except:
        pass

    app.run(debug=True, host='0.0.0.0', port=5001)
