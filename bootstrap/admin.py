import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from flask import Blueprint, render_template, request, redirect, url_for
from server.boto3 import *
from models.instance import Instance
from models.user import User
from settings import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

region_name = os.getenv('REGION_NAME')

# creating user obj
user_obj = User()
ins_obj = Instance()

instanceList = []
userList = []


@admin_bp.route('/')
def admin():
    # if is_valid_request():
    return show_instances(region_name)
    # instanceList = ins_obj.get_all_instances(region_name)
    # userList = user_obj.get_all_users()
    # return render_template('admin.html', instances=instanceList, users=userList, region_list=regions_list)


def get_admin_id():
    users = db.session.query(User)
    for admin in users:
        if admin.admin:
            return admin.id
    return "None"


@admin_bp.route('/region', methods=['GET', 'POST'])
def get_aws_instances():
    if request.method == "POST":
        if is_valid_request():
            print("requrest is valid")
            if request.form['update'] == 'aws_call':
                reg = request.form.get('reg')
                # get aws instances
                ins_list = get_instances_details(reg)
                store_instance_into_db(ins_list)
                print("aws call")
                # userList = user_obj.get_all_users()
                return show_instances(reg)
            elif request.form['update'] == 'db_call':
                print("db call")
                reg = request.form.get('reg')
                return show_instances(reg)
        return redirect(url_for('auth.auth'))
    else:
        return redirect(url_for('admin.admin'))


def show_instances(region):
    instanceList = ins_obj.get_all_instances(region)
    userList = user_obj.get_all_users()
    return render_template('admin.html', instances=instanceList, users=userList, region_list=regions_list)


@admin_bp.route('/adduser', methods=['GET', 'POST'])
def register_user():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        admin = request.form.get('admin')
        if admin == 'on':
            madmin = True
        else:
            madmin = False
        if is_valid_request():
            # store them into db
            user_obj.addUser(username=username, password=password, admin=madmin)
            return redirect(url_for('admin.admin'))
        return redirect(url_for('auth.auth'))
    else:
        return redirect(url_for('admin.admin'))


def is_valid_request():
    utoken = request.cookies.get('auth_token')
    # get current uid
    uid = get_admin_id()
    if not isinstance(uid, str):
        if User.validate_token(utoken, uid):
            return True
        return False
    return False


@admin_bp.route('/assignInstance', methods=['GET', 'POST'])
def assign_instance_to_user():
    if request.method == "POST":
        uid = request.form.get('u_id')
        insid = request.form.get('ins_id')
        uname = request.form.get('u_name')
        if is_valid_request():
            uid = get_user_id_from_db(uid)
            # store them into db
            ins_obj.assign_instance_to_user(userId=uid, ins_Id=insid)
            return redirect(url_for('admin.admin'))
        return redirect(url_for('auth.auth'))
    else:
        return redirect(url_for('admin.admin'))


@admin_bp.route('/', methods=['GET', 'POST'])
def instance_management():
    instanceList = []
    userList = user_obj.get_all_users()
    if request.method == "POST":
        if is_valid_request():
            if request.form['ins_btn'] == 'all_ins':
                # get instances data from db
                instanceList = ins_obj.get_all_instances(region_name)
            elif request.form['ins_btn'] == 'assign_ins':
                instanceList = ins_obj.get_instances_with_owner()
            elif request.form['ins_btn'] == 'assign_to':
                instanceList = ins_obj.get_all_instances()
            elif request.form['ins_btn'] == 'remove_user':
                instanceList = ins_obj.get_all_instances()
            return render_template('admin.html', instances=instanceList, users=userList, region_list=regions_list)
        return redirect(url_for('auth.auth'))
    else:
        return redirect(url_for('admin.admin'))


@admin_bp.route('/delete', methods=['GET', 'POST'])
def delete_user():
    if request.method == "POST":
        user_name = request.form['user_name']
        user_id = request.form['user_id']
        if is_valid_request():
            # delete user method call
            user_obj.deleteUser(user_id)
            return redirect(url_for('admin.admin'))
        return redireBlueprintct(url_for('auth.auth'))
    return redirect(url_for('admin.admin'))


def store_instance_into_db(instanceList):
    for i in instanceList:
        ins_obj = Instance()
        ins_obj.add_instance(i['Id'], i['Name'], i['State'], i['PublicIP'], i['PrivateIP'], i['KeyName'],
                             i['RegionName'])


def get_instance_from_db():
    return Instance().get_all_instances()

def get_user_id_from_db(username):
    userobj = db.session.query(User)
    for user in userobj:
        if user.name == username:
            return user.id
