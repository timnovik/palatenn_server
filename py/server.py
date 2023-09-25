from flask import Flask, render_template, request
from hashlib import sha256
from main import *


app = Flask(__name__, template_folder="../templates")

@app.route('/admin', methods=['post', 'get'])
def admin():
    msg = ''
    if request.method == 'POST':
        query_type = request.form.get('type')
        query = request.form.get('query')
        key = request.form.get('key')
        if sha256(key.encode()).hexdigest() == ADMIN_KEY_HASH:
            if query_type == "view":
                s_query = query.split()
                if s_query[0] == "region":
                    if len(s_query) > 1:
                        id_ = int(s_query[1])
                        if len(s_query) > 2:
                            field = s_query[2]
                            msg = str(controller.regions[id_].get(field))
                        else:
                            msg = str(controller.regions[id_])
                    else:
                        for region in controller.regions.values():
                            msg += str(region) + "<br>"

                if s_query[0] == "state":
                    if len(s_query) > 1:
                        id_ = int(s_query[1])
                        if len(s_query) > 2:
                            field = s_query[2]
                            msg = str(controller.states[id_].get(field))
                        else:
                            msg = str(controller.states[id_])
                    else:
                        for state in controller.states.values():
                            msg += str(state) + "<br>"

                if s_query[0] == "province":
                    if len(s_query) > 1:
                        id_ = int(s_query[1])
                        if len(s_query) > 2:
                            field = s_query[2]
                            msg = str(controller.provinces[id_].get(field))
                        else:
                            msg = str(controller.provinces[id_])
                    else:
                        for province in controller.provinces.values():
                            msg += str(province) + "<br>"

            elif query_type == "build":
                controller.add_action(eval(f"Action(ActionEnum.build, BuildActionData(BuildingEnum.{query}))"))
            elif query_type == "commit":
                status, state = controller.commit()
                msg = str((status.name, state))
        else:
            raise KeyError(f"sha256(\"{key}\")={hash(key)}!={ADMIN_KEY_HASH}")
    return render_template('admin.html', msg=msg)


if __name__ == '__main__':
    app.run(port=HOST_PORT, host=HOST_IP)

