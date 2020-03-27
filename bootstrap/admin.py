from flask import Blueprint, render_template
from .server.boto3 import *
from .models.instance import Instance
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
from .user import User
region_name = os.getenv('REGION_NAME')

@admin_bp.route('/')
@admin_bp.route('/region/<reg_name>')
def admin(reg_name=region_name):
    # query data from aws
    instanceList = get_instances_details(reg_name)

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
    userList = []
    for i in range(0, 3):
        userDict = {
            "ID": 1234,
            "Name": "M Imtiaz",
        }
        userList.append(userDict)

    return render_template('admin.html', instances=instanceList, users=userList, region_list=regions_list)

def store_instance_into_db(instanceList):
    # print(instanceList)
    for i in instanceList:
        ins_obj = Instance()
        ins_obj.add_instance(i['Id'], i['Name'], i['State'], i['PublicIP'], i['PrivateIP'],  i['KeyName'])


def get_instance_from_db():
    return Instance().get_all_instances()
