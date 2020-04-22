import os
import sys
import time
import threading
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from flask import Blueprint, render_template, jsonify, json, redirect, request, url_for
from server.boto3 import *
from models.instance import Instance
from models.user import User, BlacklistToken
from settings import db
from admin import get_instances_details, store_instance_into_db



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
            user_regions = set({})
            for instance in instanceList:
                user_regions.add(instance['RegionName'])
            for region_name in user_regions:
                update_thread = threading.Thread(target=update_instance_in_db, args=(region_name, ))
                update_thread.start()
    return render_template('user.html', instances=instanceList, region_list=all_regions)


@user_bp.route('/change', methods=['POST'])
def change_ins_state():
    if request.method == "POST":
        id = request.form['instance_id']
        state = request.form['instance_state']
        region_name = request.form['region_name']
        utoken = request.cookies.get('auth_token')
        uid = get_uid()

        if not isinstance(uid, str):
            if User.validate_token(utoken, uid):
                if state == 'stopped':
                    start_instance(id, region_name)
                elif state == 'running':
                    stop_instance(id, region_name)
                update_thread = threading.Thread(target=update_instance_in_db, args=(region_name, ))
                update_thread.start()
                return redirect(url_for('user.user'))

    return redirect(url_for('user.user'))

@user_bp.route('/logout', methods=['GET'])
def logout():
    utoken = request.cookies.get('auth_token')
    # get current uid
    uid = get_uid()
    if not isinstance(uid, str):
        if User.validate_token(utoken, uid):
            blacklist_token = BlacklistToken(token=utoken)
            try:
                # insert the token
                print("in the Try block")
                db.session.add(blacklist_token)
                db.session.commit()
                return render_template('login.html')
            except Exception as e:
                print(e)
                return redirect(url_for('user.user'))



def get_uid():
    utoken = request.cookies.get('auth_token')
    uid = User.decode_auth_token(utoken)
    return uid

def update_instance_in_db(region_name):
    ins_list = get_instances_details(region_name)
    store_instance_into_db(ins_list)

