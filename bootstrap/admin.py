from flask import Blueprint, render_template, request, redirect, url_for
from .server.boto3 import *
from .models.instance import Instance
from .models.user import User
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
from .user import User

region_name = os.getenv('REGION_NAME')

# creating user obj
user_obj = User()
ins_obj = Instance()

instanceList = []
userList = []

@admin_bp.route('/')
# @admin_bp.route('/region/<reg_name>')
def admin():
    # query data from aws
    instanceList = get_instances_details(region_name)

    # ins_obj = Instance()
    # instanceList = ins_obj.get_instances_with_owner()
    # print(instanceList)

    # user_obj = User()
    # user_obj.deleteUser('i-09f4e6463b38c943e')
    # user_obj.addUser('Imtiaz', 'i-09f4e6463b38c943e')
    # user_obj.assign_instance_to_user("Imtiaz", "i-09f4e6463b38c943e")
    #
    # ##
    # # Unique key constraints...
    ##

    # Store/update latest data into database
    # store_instance_into_db(instanceList)

    # # # fetch data from database
    # instanceList = get_instance_from_db()
    # print(instanceList)
    # creating users list
    # userList = []
    userList = user_obj.get_all_users()
    return render_template('admin.html', instances=instanceList, users=userList, region_list=regions_list)


@admin_bp.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        # store them into db
        user_obj.addUser(username=username, password=password)
        return redirect(url_for('admin.admin'))
    else:
        return redirect(url_for('admin.admin'))

@admin_bp.route('/', methods=['GET', 'POST'])
def instance_management():
    userList = user_obj.get_all_users()
    if request.method == "POST":
        if request.form['ins_btn'] == 'all_ins':
            # get instances data from db
            instanceList = ins_obj.get_all_instances()
        elif request.form['ins_btn'] == 'assign_ins':
            instanceList = ins_obj.get_instances_with_owner()
        elif request.form['ins_btn'] == 'assign_to':
            instanceList = ins_obj.get_all_instances()
        elif request.form['ins_btn'] == 'remove_user':
            instanceList = ins_obj.get_all_instances()
        return render_template('admin.html', instances=instanceList, users=userList, region_list=regions_list)
    else:
        return redirect(url_for('admin.admin'))


@admin_bp.route('/delete', methods=['GET', 'POST'])
def delete_user():
    if request.method == "POST":
        user_name = request.form['user_name']
        user_id = request.form['user_id']
        print(user_id, user_name)
        # delete user method call
        user_obj.deleteUser(user_id)
        print("user deleted successfully....")
        return redirect(url_for('admin.admin'))
    return redirect(url_for('admin.admin'))



def store_instance_into_db(instanceList):
    for i in instanceList:
        ins_obj = Instance()
        ins_obj.add_instance(i['Id'], i['Name'], i['State'], i['PublicIP'], i['PrivateIP'], i['KeyName'])


def get_instance_from_db():
    return Instance().get_all_instances()

