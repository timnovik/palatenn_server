from flask import Flask, render_template, request
from main import *

app = Flask(__name__, template_folder="../templates")

@app.route('/admin', methods=['post', 'get'])
def admin():
    msg = ''
    if request.method == 'POST':
        query_type = request.form.get('type')
        query = request.form.get('query')
        key = request.form.get('key')
        if key == ADMIN_KEY:
            if query_type == "view":
                s_query = query.split()
                if s_query[0] == "region":
                    if len(s_query) > 1:
                        id_ = int(s_query[1])
                        if len(s_query) > 2:
                            field = s_query[2]
                            msg = controller.regions[id_].get(field)
                        else:
                            msg = controller.regions[id_]
                    else:
                        for region in controller.regions:
                            msg += str(region) + "\n"

                if s_query[0] == "state":
                    if len(s_query) > 1:
                        id_ = int(s_query[1])
                        if len(s_query) > 2:
                            field = s_query[2]
                            msg = controller.states[id_].get(field)
                        else:
                            msg = controller.states[id_]
                    else:
                        for state in controller.states:
                            msg += str(state) + "\n"

                if s_query[0] == "province":
                    if len(s_query) > 1:
                        id_ = int(s_query[1])
                        if len(s_query) > 2:
                            field = s_query[2]
                            msg = controller.provinces[id_].get(field)
                        else:
                            msg = controller.provinces[id_]
                    else:
                        for province in controller.provinces:
                            msg += str(province) + "\n"

            elif query_type == "build":
                controller.add_action(eval(f"Action(ActionEnum.build, BuildActionData(BuildingEnum.{query}))"))
            elif query_type == "commit":
                status, state = controller.commit()
                msg = str((status.name, state))
    return render_template('admin.html', msg=msg)


if __name__ == '__main__':
    app.run(port=HOST_PORT, host=HOST_IP)

