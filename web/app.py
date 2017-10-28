from sanic import Sanic
from sanic.response import json
from sanic.views import HTTPMethodView
from model import get_node_by_id, get_all_nodes, create_node, get_location_by_url, get_graph_under_location
from sanic.response import text
from json import dumps
app = Sanic("Node_Manager")

@app.route("/")
async def root(request):
    return text("Front page goes here")



@app.route("/node/<uid>/sensors")
async def show_sensors(request, uid):
    x = get_node_by_id(uid).get('sensors')
    return json(x)

@app.route("/node/<uid>/sensors/<sid>")
async def show_sensor(request, uid, sid):
    x = get_node_by_id(uid).sensors
    return json(x)


class Node(HTTPMethodView):
    async def get(self, request):
        nodes = get_all_nodes()
        return json({"hello": "world", "nodes": nodes})

    async def post(self, request):
        print("creating new node")
        data = request.json
        print(data)
        name = data['name']
        # location = data['location']
        location_url = data['location_url']
        lat = data['lat']
        lon = data['lon']
        tags = ", ".join(data['tags'])
        new_node = create_node(name, location_url, lat, lon, tags)
        return(json({"status":"success",
                     "redirect_url":app.url_for('NodeID', node_id=str(new_node.uid.decode("utf-8") ))}))
app.add_route(Node.as_view(), '/node/')

class NodeID(HTTPMethodView):
    async def get(self, request, node_id):
        this_node = get_node_by_id(node_id)
        # this_node['location'] = this_node['location'].url  # Hack to prevent deep recursion into location graph
        return json(this_node)

    async def put(self, request, node_id):
        # TODO code for modifying node
        return text('I am put method for node {}'.format(node_id))

    async def delete(self, request, node_id):
        # TODO code for deleting node
        return text('I am delete method for node {}'.format(node_id))
app.add_route(NodeID.as_view(), '/node/<node_id>')



class SensorID(HTTPMethodView):
    async def get(self, request, node_id, sensor_id):
        # No need to get all sensors for a node, get node/node_id does that
        # This is more for manipulating single sensors, viewing their data
        this_node = get_node_by_id(node_id)
        return text('I am get method for node {} sensor {}'.format(node_id, sensor_id))
        return json(this_node)

    async def put(self, request, node_id, sensor_id):
        # TODO code for modifying node
        return text('I am put method for node {} sensor {}'.format(node_id, sensor_id))

    async def delete(self, request, node_id, sensor_id):
        # TODO code for deleting node
        return text('I am delete method for node {} sensor {}'.format(node_id, sensor_id))
app.add_route(SensorID.as_view(), '/node/<node_id>/sensor/<sensor_id>')


class Location(HTTPMethodView):
    async def get(self, request):
        loc_url = request.args.get('loc_url')
        location = get_location_by_url(loc_url)
        location_data = location.to_json()
        child_graph = get_graph_under_location(location)
        print(child_graph)
        return text(dumps({'location_data': location_data,
                            'child_graph': child_graph}))
        # return text('I am get method for location {}'.format(loc_url))

    async def post(self, request):
        # TODO code for creating location
        return text('I am post method for location {}'.format(loc_url))

    async def put(self, request):
        # TODO code for modifying location
        return text('I am put method for location {}'.format(loc_url))

    async def delete(self, request):
        # TODO code for deleting location
        return text('I am delete method for location {}'.format(loc_url))
app.add_route(Location.as_view(), '/location')





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
