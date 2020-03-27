from flask import Blueprint, render_template, jsonify, json
from .server.boto3 import *
from .models.user import User
from .models.instance import Instance

user_bp = Blueprint('user', __name__, url_prefix='/user')
region_name = os.getenv('REGION_NAME')


@user_bp.route('/')
def user():
    instanceList = get_instances_details(region_name)
    return render_template('user.html', instances=instanceList, region_list=all_regions)

@user_bp.route('/', methods=('GET', 'POST'))
def addUser():
    pass