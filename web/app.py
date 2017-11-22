from sanic import Sanic
from sanic.response import json
from pony.orm import db_session, select
from models import Nodule, Component, Job, Zone
from sanic.response import text, json
from sanic.exceptions import abort
from yaml import dump as ydump
from json import dumps as jdump
app = Sanic("Node Config Manager")


def get_nodule(n_id):
    print("Fetching config for {}".format(n_id))
    with db_session:
        nodule = Nodule.get(uid=n_id)
        if not nodule:
            abort(404)
        print("Found nodule: {}".format(nodule.name))
        return nodule

def get_model(resource):
    lookup = {
        'jobs': Job,
        'components': Component,
        'sensors': Component,
        'actuators': Component,
        'nodule': Nodule
    }
    model = lookup.get(resource)
    if not model:
        print("Resource {} not known".format(resource))
        abort(400)
    return model

def get_items(model, nodule):
    with db_session:
        items = select(x for x in model if x.nodule==nodule)[:]
        print("Found {} {}s".format(len(items), model.__name__))
        columns = model._columns_
        data = []
        for item in items:
            d = {c: getattr(item, c) for c in columns if type(getattr(item, c)) in [str, int, bool]}
            if model==Job:
                component = item.component.uid
                d['component'] = component
            data.append(d)
        # print(data)
    return data

def get_nodule_info(nodule):
    columns = Nodule._columns_
    data = {c: getattr(nodule, c) for c in columns if type(getattr(nodule, c)) in [str, int, bool]}
    default_data = {'valid_pins': [],
                    'manager': {'url': '127.0.0.1', 'port':'8888',
                                'get_config_endpoints': {'nodule': 'nodule/{n_id}/nodule',
                                             'hardware': 'nodule/{n_id}/hardware',
                                             'sensors': 'nodule/{n_id}/sensors',
                                             'actuators': 'nodule/{n_id}/actuators',
                                             'jobs': 'nodule/{n_id}/jobs'}},
                    'mqtt': {'url': '127.0.0.1', 'port': '1883', 'keepalive': '1883'},
                    'topics': ['sensors', 'logs', 'errors', 'report', 'presence'],
                    }
    data.update(default_data)
    return data

def filter_components(data, kind):
    kind_name = {'sensors': 'sensor', 'actuators': 'actuator'}.get(kind)
    data = [d for d in data if d.get('kind') == kind_name]
    return data



@app.route("/")
async def root(request):
    return text("Front page goes here")

@app.route("/nodule/")
async def all_nodules(request):
    # Just return a list of nodule uids
    with db_session:
        nodules = select(n for n in Nodule)
        data = [n.uid for n in nodules]
    return json(data)

@app.route("/nodule/<n_id:[A-z0-9]{6}>/")
async def nodule_resources(request, n_id):
    return text("TODO: Links to resources should go here...")

@app.route("/nodule/<n_id:[A-z0-9]{6}>/nodule")
async def nodule_config(request, n_id):
    nodule = get_nodule(n_id)
    data = get_nodule_info(nodule)
    return text(jdump(data))

@app.route("/nodule/<n_id:[A-z0-9]{6}>/<resource>")
async def resource_config(request, n_id, resource):
    model = get_model(resource)
    nodule = get_nodule(n_id)
    data = get_items(model, nodule)
    if resource in ['sensors', 'actuators']:
        data = filter_components(data, resource)
    # if resource == 'jobs':
    #     data = link_job_to_component(data)
    return text(jdump(data))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
