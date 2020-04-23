import os
import sys
import threading
from flask import Blueprint, render_template, request, redirect, url_for

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from server.aws import get_instances_details, get_all_regions
from models.instance import Instance
from models.user import User, BlacklistToken
from settings import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
region_name = os.getenv('REGION_NAME')

# creating user obj
user_obj = User()
instance_obj = Instance()

# instances_list = []
# users_list = []


@admin_bp.route('/instances', methods=['GET'])
def get_admin():
    # if is_valid_request():
    update_thread = threading.Thread(target=make_aws_call, args=())
    update_thread.start()
    return get_instances()
    # return render_template('login.html')


@admin_bp.route('/users')
def get_users():
    users_list = user_obj.get_all_users()
    return render_template('user-management.html', users=users_list)


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
        print("IDSS", user_id, insid)
        if is_valid_request():
            instance_obj.un_assign_instance_from_user(user_id=user_id, instance_id=insid)
            print("method called")
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
    return render_template('admin.html', assigned_instances=assigned_instances, instances=instances_list)


def is_valid_request():
    user_token = request.cookies.get('auth_token')
    print(user_token, " u token")
    # get current user_id
    user_id = get_admin_id()
    print(user_id, " admin ID")
    if not isinstance(user_id, str):
        if User.validate_token(user_token, user_id):
            return True
        return False
    return False


def make_aws_call():
    regions_list = get_all_regions()
    for region in regions_list:
        ins_list = get_instances_details(region)
        # print(ins_list)
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


def get_instance_from_db():
    return Instance().get_all_instances()


def get_user_id_from_db(username):
    userobj = db.session.query(User)
    for user in userobj:
        if user.name == username:
            return user.id
    return None
