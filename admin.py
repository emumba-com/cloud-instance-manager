import os
import sys
import threading
import schedule
import time
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from server.aws import (get_instances_details,
                        get_all_regions, get_untagged_instances,
                        attach_tag_to_instances, get_instances_daily_cost,
                        get_instances_monthly_cost)
from models.instance import Instance
from models.ssh_keys import SSHKeys
from models.user import User, BlacklistToken
from models.cost_explorer import CostExplorer
from settings import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
region_name = os.getenv('REGION_NAME')

# creating user obj
user_obj = User()
instance_obj = Instance()
ssh_key_obj = SSHKeys()
ce_obj = CostExplorer()


@admin_bp.route('/instances', methods=['GET'])
def get_admin():
    # my_thread = threading.Thread(target=tag_all_ec2_instances, args=())
    # my_thread.start()
    # if is_valid_request():
    update_thread = threading.Thread(target=make_aws_call, args=())
    update_thread.start()
    return get_instances()
    # return render_template('login.html')


@admin_bp.route('/ssh-keys')
def get_ssh_keys():
    keys_list, all_keys_list = ssh_key_obj.get_ssh_keys_from_db()
    return render_template('ssh-keys.html',
                           keys_list=keys_list,
                           all_keys_list=all_keys_list)


@admin_bp.route('/users')
def get_users():
    users_list = user_obj.get_all_users()
    return render_template('user-management.html', users=users_list)


@admin_bp.route('/addkey', methods=['GET', 'POST'])
def register_key():
    if request.method == "POST":
        key_name = request.form.get('keyname')
        key_value = request.form.get('keyvalue')
        key_format = request.form.get('keyformat')
        ssh_key_obj.add_ssh_key_value(key_name, key_value, key_format)
    return redirect(url_for('admin.get_ssh_keys'))


@admin_bp.route('/adduser', methods=['GET', 'POST'])
def register_user():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        admin = request.form.get('admin')
        admin_flag = admin == 'on'
        if is_valid_request():
            # store them into db
            user_obj.add_user(username=username, password=password, admin=admin_flag)
            return redirect(url_for('admin.get_users'))
        return redirect(url_for('auth.auth'))
    return redirect(url_for('admin.get_users'))


@admin_bp.route('/assignInstance', methods=['POST'])
def assign_instance_to_user():
    if request.method == "POST":
        user_id = request.form.get('user_id')
        insid = request.form.get('inst_id')
        if is_valid_request():
            user_id = get_user_id_from_db(user_id)
            # store them into db
            instance_obj.assign_instance_to_user(user_id=user_id, instance_id=insid)
            return redirect(url_for('admin.get_admin'))
        return redirect(url_for('auth.auth'))
    return redirect(url_for('admin.get_admin'))


@admin_bp.route('/un_assignInstance', methods=['POST'])
def un_assign_instance_to_user():
    if request.method == "POST":
        user_id = request.form.get('un_user_id')
        insid = request.form.get('un_inst_id')
        if is_valid_request():
            instance_obj.un_assign_instance_from_user(user_id=user_id, instance_id=insid)
            return redirect(url_for('admin.get_admin'))
        return redirect(url_for('auth.auth'))
    return redirect(url_for('admin.get_admin'))


@admin_bp.route('/', methods=['POST'])
def instance_management():
    if request.method == "POST":
        if is_valid_request():
            if request.form['ins_btn'] == 'assigned_ins':
                assigned_instances = instance_obj.get_assigned_instances()
                return render_template('admin.html', instances=assigned_instances)
            return redirect(url_for('admin.get_admin'))
        return redirect(url_for('auth.auth'))
    return redirect(url_for('admin.get_admin'))


@admin_bp.route('/users/delete', methods=['GET', 'POST'])
def delete_user():
    if request.method == "POST":
        user_id = request.form['user_id']
        if is_valid_request():
            # delete user method call
            instance_obj.delete_user(user_id)
            return redirect(url_for('admin.get_users'))
        return redirect(url_for('auth.auth'))
    return redirect(url_for('admin.get_users'))


@admin_bp.route('/delete_key', methods=['GET', 'POST'])
def delete_key():
    if request.method == "POST":
        key_id = request.form['key_id']
        if is_valid_request():
            # delete key method call
            ssh_key_obj.delete_key(key_id)
            return redirect(url_for('admin.get_ssh_keys'))
        return redirect(url_for('auth.auth'))
    return redirect(url_for('admin.get_ssh_keys'))


@admin_bp.route('/logout', methods=['GET'])
def logout_admin():
    # if is_valid_request():
    admin_token = request.cookies.get('auth_token')
    blacklisted_token = BlacklistToken(token=admin_token)
    try:
        db.session.add(blacklisted_token)
        db.session.commit()
        return render_template('login.html')
    except Exception as db_exception:
        print(db_exception)
        return redirect(url_for('admin.get_admin'))


@admin_bp.route('/bill', methods=['GET'])
def get_admin_bill():
    return get_cost_from_db()


def fetch_instances_cost_from_aws():
    monthly_cost = get_instances_monthly_cost(str(get_first_date()), str(get_today_date()))
    daily_cost = get_instances_daily_cost(str(get_yesterday_date()), str(get_today_date()))
    delete_terminated_instances_cost(monthly_cost)
    store_instances_cost_into_db(monthly_cost, daily_cost)


def store_instances_cost_into_db(monthly_cost, daily_cost):
    for m_cost in monthly_cost:
        ce_obj.add_monthly_bill(m_cost['CE_INS_KEY'], m_cost['CE_INS_COST'])
    for d_cost in daily_cost:
        ce_obj.add_daily_bill(d_cost['CE_INS_KEY'], d_cost['CE_INS_COST'])


def get_cost_from_db():
    response = ce_obj.get_complete_bill_from_db()
    return render_template('admin-billing.html', all_instances_cost=response)


def get_admin_id():
    users = db.session.query(User)
    for admin in users:
        if admin.admin:
            return admin.id
    return "None"


def get_instances():
    instances_list = instance_obj.get_all_instances_from_db()
    # sending assigned user's data..
    assigned_instances = instance_obj.get_assigned_instances()
    return render_template('admin.html',
                           assigned_instances=assigned_instances,
                           instances=instances_list)


def is_valid_request():
    user_token = request.cookies.get('auth_token')
    user_id = get_admin_id()
    if not isinstance(user_id, str):
        return User.validate_token(user_token, user_id)
    return False


def make_aws_call():
    regions_list = get_all_regions()
    for region in regions_list:
        ins_list = get_instances_details(region)
        delete_terminated_instances(ins_list, region)
        store_instance_into_db(ins_list)


def store_instance_into_db(instances_list):
    for instance in instances_list:
        instance_obj.add_instance(instance['Id'],
                                  instance['Name'],
                                  instance['State'],
                                  instance['PublicIP'],
                                  instance['PrivateIP'],
                                  instance['KeyName'],
                                  instance['RegionName'])


def delete_terminated_instances(aws_instances_list, region):
    db_instances_list = Instance.query.filter_by(region_name=region)
    db_instances_ids = [instance.id for instance in db_instances_list]
    aws_instances_ids = [instance['Id'] for instance in aws_instances_list]
    ins_not_exists = list(set(db_instances_ids) - set(aws_instances_ids))
    ins_not_exists = [db_ins_id for db_ins_id in db_instances_ids if db_ins_id not in aws_instances_ids]
    if ins_not_exists:
        instance_obj.delete_instance_from_db(ins_not_exists)


def delete_terminated_instances_cost(aws_monthly_cost_list):
    db_instances_cost_list = CostExplorer.query.all()
    db_instances_ids = [instance.ce_instance_id for instance in db_instances_cost_list]
    aws_instances_ids = [instance['CE_INS_KEY'] for instance in aws_monthly_cost_list]
    print('DB instances: ', db_instances_cost_list, '\n\n')
    print('aws instances: ', aws_instances_ids, '\n\n')
    ins_not_exists = list(set(db_instances_ids) - set(aws_instances_ids))
    ins_not_exists = [db_ins_id for db_ins_id in db_instances_ids if db_ins_id not in aws_instances_ids]
    print(ins_not_exists)
    if ins_not_exists:
        ce_obj.delete_instance_cost_from_db(ins_not_exists)


def get_user_id_from_db(username):
    userobj = db.session.query(User)
    for user in userobj:
        if user.name == username:
            return user.id
    return None


def tag_ec2_instance_of_region(region):
    instance_tags_list = []
    instance_tags_list = get_untagged_instances(region)
    attach_tag_to_instances(instance_tags_list)


def tag_all_ec2_instances():
    regions_list = get_all_regions()
    for region in regions_list:
        tag_ec2_instance_of_region(region)


def get_today_date():
    return datetime.utcnow().strftime('%Y-%m-%d')


def get_first_date():
    return datetime.utcnow().replace(day=1).strftime('%Y-%m-%d')


def get_yesterday_date():
    return (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
