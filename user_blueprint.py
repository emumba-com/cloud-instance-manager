import os
import sys
import threading
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
from flask import Blueprint, render_template, redirect, request, url_for
from server.aws import get_all_regions, start_instance, stop_instance
from models.instance import Instance
from models.ssh_keys import SSHKeys
from models.cost_explorer import CostExplorer
from models.user import User, BlacklistToken
from settings import db
from admin import get_instances_details, store_instance_into_db

user_bp = Blueprint('user', __name__, url_prefix='/user')

instance_obj = Instance()
user_obj = User()
ssh_key_obj = SSHKeys()
ce_obj = CostExplorer()


@user_bp.route('/')
def user():
    instances_list = []
    # getting ssh keys info
    ssh_keys = ssh_key_obj.get_ssh_keys_from_db()
    all_keys_list = ssh_keys[1]
    user_token = request.cookies.get('auth_token')
    # get current user_id
    user_id = get_user_id()
    if not isinstance(user_id, str):
        if User.validate_token(user_token, user_id):
            instances_list = instance_obj.get_user_instances(user_id)
            user_regions = set({})
            for instance in instances_list:
                user_regions.add(instance['RegionName'])
            for region_name in user_regions:
                update_thread = threading.Thread(target=update_instance_in_db, args=(region_name, ))
                update_thread.start()
    return render_template('user.html',
                           instances=instances_list, all_keys_list=all_keys_list, region_list=get_all_regions)


@user_bp.route('/change', methods=['POST'])
def change_ins_state():
    if request.method == "POST":
        instance_id = request.form['instance_id']
        state = request.form['instance_state']
        region_name = request.form['region_name']
        user_token = request.cookies.get('auth_token')
        user_id = get_user_id()

        if not isinstance(user_id, str):
            if User.validate_token(user_token, user_id):
                if state == 'stopped':
                    start_instance(instance_id, region_name)
                elif state == 'running':
                    stop_instance(instance_id, region_name)
                update_thread = threading.Thread(target=update_instance_in_db, args=(region_name, ))
                update_thread.start()
                return redirect(url_for('user.user'))

    return redirect(url_for('user.user'))


@user_bp.route('/logout', methods=['GET'])
def logout():
    user_token = request.cookies.get('auth_token')
    # get current user_id
    user_id = get_user_id()
    if not isinstance(user_id, str):
        if User.validate_token(user_token, user_id):
            blacklist_token = BlacklistToken(token=user_token)
            try:
                db.session.add(blacklist_token)
                db.session.commit()
                return render_template('login.html')
            except Exception as db_exception:
                print(db_exception)
    return redirect(url_for('user.user'))


@user_bp.route('/bill', methods=['GET'])
def get_user_bill():
    user_instances_cost = []
    user_id = get_user_id()
    instances_list = instance_obj.get_user_instances(user_id)
    all_instances_cost = ce_obj.get_complete_bill_from_db()
    for ins in instances_list:
        cost_exist = True
        for cost in all_instances_cost:
            if ins['Id'] == cost['Id']:
                user_instances_cost.append(cost)
                cost_exist = False
                break
        if cost_exist:
            ins_no_cost = {
                "Id": ins['Id'],
                "Name": ins['Name'],
                "DailyBill": '0.0',
                "MonthlyBill": '0.0'
            }
            user_instances_cost.append(ins_no_cost)
    return render_template('user-billing.html', user_bill=user_instances_cost)


def get_user_id():
    user_token = request.cookies.get('auth_token')
    user_id = User.decode_auth_token(user_token)
    return user_id


def update_instance_in_db(region_name):
    ins_list = get_instances_details(region_name)
    store_instance_into_db(ins_list)
