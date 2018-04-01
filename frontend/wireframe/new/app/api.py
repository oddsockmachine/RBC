import time
from datetime import datetime
from flask import Flask, jsonify, request
from flask import render_template
from werkzeug.contrib.cache import SimpleCache
from random import randint, seed
import time
import json

seed()

app = application = Flask("VueFlask")
cache = SimpleCache()

todos = [
    { 'id': 0, 'text': 'Vegetables', 'time': 1499312488084 },
    { 'id': 1, 'text': 'Cheese', 'time': 1499312488084 },
    { 'id': 2, 'text': 'Whatever else humans are supposed to eat', 'time': 1499312488084 }
]

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/environments")
def environments():
    return render_template('environments.html')

@app.route("/new_env")
def new_env():
    return render_template('new_env.html')


@app.route("/api/one")
def one():
    o = cache.get("one")
    if not o:
        o = {"one": list(range(10))}
        cache.set("one", o, timeout=30)
    return jsonify(o)


@app.route("/api/two")
def two():
    return jsonify(
        {
            "two": [randint(10,20) for k in range(10, 20)]
        }
    )


@app.route("/api/all", methods=['GET'])
def all():
    data = todos.copy()
    for t in data:
        t['time'] = time.time() - t['time']
    return jsonify(data)

@app.route("/api/add", methods=['POST'])
def add():
    data = json.loads(request.data)
    new_todo = data.get('newTodo')
    new_ID = data.get('id')
    print(new_todo, new_ID)
    todos.append({ 'id': new_ID, 'text': new_todo, 'time': int(time.time()) })
    return jsonify(
        {
            "status": 'added successfully',
            "new todo was": new_todo
        }
    )


# @app.route("/healthz")
# def healthz():
#     return jsonify(
#         {
#             "flask": True,
#             "global": True
#         }
#     )


@app.route("/api/ts")
def ts():
    return jsonify(
        {
            "now": "foo: " + str(datetime.now())
        }
    )


if __name__ == '__main__':
    app.run(debug=True)
