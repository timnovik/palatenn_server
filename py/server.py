from flask import Flask
from main import *

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, world!'


@app.route('/view_province/<int:province_id>')
def province_view(province_id):
    return str(provinces[int(province_id)])


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')

