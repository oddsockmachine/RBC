from sanic import Sanic
from sanic.response import json
from pony.orm import db_session, select
from ponypostgres import Nodule, Component, Job, Zone
from sanic.response import text, json
from sanic.exceptions import abort
from yaml import dump as ydump
from json import dumps as jdump
app = Sanic("Node_Manager")

@app.route("/")
async def root(request):
    return text("Front page goes here")

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
        data = [{c: getattr(item, c) for c in columns if type(getattr(item, c)) in [str, int]} for item in items]
        print(data)
    return data

def filter_components(data, kind):
    data = [d for d in data if d.get('kind') == kind]
    return data

@app.route("/nodule/<n_id:[A-z0-9]{6}>/")
async def nodule_config(request, n_id):
    return text("TODO: Links to resources should go here...")


@app.route("/nodule/<n_id:[A-z0-9]{6}>/jobs")
async def nodule_config(request, n_id):
    model = get_model('jobs')
    nodule = get_nodule(n_id)
    data = get_items(model, nodule)
    return text(ydump(data))

@app.route("/nodule/<n_id:[A-z0-9]{6}>/components")
async def nodule_config(request, n_id):
    model = get_model('components')
    nodule = get_nodule(n_id)
    data = get_items(model, nodule)
    return text(ydump(data))

@app.route("/nodule/<n_id:[A-z0-9]{6}>/sensors")
async def nodule_config(request, n_id):
    model = get_model('components')
    nodule = get_nodule(n_id)
    data = get_items(model, nodule)
    data = filter_components(data, 'sensor')
    return text(ydump(data))

@app.route("/nodule/<n_id:[A-z0-9]{6}>/actuators")
async def nodule_config(request, n_id):
    model = get_model('components')
    nodule = get_nodule(n_id)
    data = get_items(model, nodule)
    data = filter_components(data, 'actuator')
    return text(ydump(data))

@app.route("/nodule/<n_id:[A-z0-9]{6}>/<resource>")
async def nodule_config(request, n_id, resource):
    model = get_model(resource)
    nodule = get_nodule(n_id)
    data = get_items(model, nodule)
    return text(ydump(data))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
