from flask import Blueprint, render_template, jsonify, json, redirect, request, url_for
from .server.boto3 import *
from .models.instance import Instance
from .models.user import User

from .server.boto3 import stop_instance
from .server.boto3 import start_instance

user_bp = Blueprint('user', __name__, url_prefix='/user')
region_name = os.getenv('REGION_NAME')

instance_obj = Instance()
user_obj = User()

@user_bp.route('/')
def user():
    instanceList = []
    utoken = request.cookies.get('auth_token')
    # get current uid
    uid = get_uid()
    if not isinstance(uid, str):
        if User.validate_token(utoken, uid):
            instanceList = instance_obj.get_user_instances(uid)
    return render_template('user.html', instances=instanceList, region_list=all_regions)


@user_bp.route('/change', methods=['GET', 'POST'])
def change_ins_state():
    if request.method == "POST":
        id = request.form['instance_id']
        state = request.form['instance_state']
        region_name = request.form['region_name']

        uid = get_uid()

        if not isinstance(uid, str):
            if User.validate_token(uid):
                if state == 'stopped':
                    start_instance(id, region_name)
                    print("instance started")
                elif state == 'running':
                    print("instance started")
                    stop_instance(id, region_name)
                return redirect(url_for('user.user'))

    return redirect(url_for('user.user'))

def get_uid():
    utoken = request.cookies.get('auth_token')
    uid = User.decode_auth_token(utoken)
    return uid