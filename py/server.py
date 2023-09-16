from flask import Flask
from main import *

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, world!'


@app.route('/province/<int:province_id>')
def province_view(province_id):
    return str(provinces[province_id])


@app.route('/province/<int:province_id>/<string:attr>')
def province_attr_view(province_id, attr):
    return str(provinces[province_id].get(attr))


@app.route('/state/<int:state_id>')
def state_view(state_id):
    return str(states[state_id])


@app.route('/state/<int:state_id>/<string:attr>')
def state_attr_view(state_id, attr):
    return str(states[state_id].get(attr))


@app.route('/region/<int:region_id>')
def region_view(region_id):
    return str(regions[region_id])


@app.route('/region/<int:region_id>/<string:attr>')
def region_attr_view(region_id, attr):
    return str(regions[region_id].__getattribute__(attr))


if __name__ == '__main__':
    app.run(port=HOST_PORT, host=HOST_IP)

