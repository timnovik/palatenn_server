from flask import Flask, render_template, request
from main import *

app = Flask(__name__, template_folder="../templates")


@app.route('/')
def hello():
    return 'Hello, world!'


@app.route('/province/<int:province_id>')
def province_view(province_id):
    return str(controller.provinces[province_id])


@app.route('/province/<int:province_id>/<string:attr>')
def province_attr_view(province_id, attr):
    return str(controller.provinces[province_id].get(attr))


@app.route('/state/<int:state_id>')
def state_view(state_id):
    return str(controller.states[state_id])


@app.route('/state/<int:state_id>/<string:attr>')
def state_attr_view(state_id, attr):
    res = controller.states[state_id].get(attr)
    if callable(res):
        return str(res())
    return str(res)


@app.route('/region/<int:region_id>')
def region_view(region_id):
    return str(controller.regions[region_id])


@app.route('/region/<int:region_id>/<string:attr>')
def region_attr_view(region_id, attr):
    return str(controller.regions[region_id].get(attr))


@app.route('/admin', methods=['post', 'get'])
def admin():
    msg = ''
    if request.method == 'POST':
        query_type = request.form.get('type')
        query = request.form.get('query')
        key = request.form.get('key')
        if key == ADMIN_KEY:
            if query_type == "build":
                controller.add_action(eval(f"Action(ActionEnum.build, BuildActionData(BuildingEnum.{query}))"))
            elif query_type == "commit":
                status, state = controller.commit()
                msg = str((status.name, state))
    return render_template('admin.html', msg=msg)


if __name__ == '__main__':
    app.run(port=HOST_PORT, host=HOST_IP)

