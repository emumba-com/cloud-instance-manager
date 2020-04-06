import bcrypt
from .models.user import User
from flask import make_response, Blueprint, render_template, request, jsonify, redirect, url_for
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
user_obj = User()
from .app import db
from .config import DevelopmentConfig


@auth_bp.route('/')
def auth():
    return render_template('login.html')


@auth_bp.route('/signin', methods=['GET', 'POST'])
def login():
    admin = 'off'
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = request.form.get('admin')
        print(admin, "admin checkbox")
        print(username, password)
        try:
            # get user from db
            user = User.query.filter_by(user.name=username).first()
            # TODO if condition for user existance

            auth_token = user_obj.encode_auth_token(user.id)

            if bcrypt.check_password_hash(user.password, password):
                #TODO: Add generated token to cockies
                if user.admin == 'true' and admin == 'on':
                    resp = make_response(render_template('admin.html'))
                    return resp
                resp = make_response(render_template('user.html'))
                return resp
            # TODO
            # else:
            #     # need to generate new token for that user...
            #     resp = make_response(render_template('login.html'))
            #     return resp
        except Exception as e:
            # TODO: Add internal server error message incase of exception.
            print(e)
            resp = make_response(render_template('login.html'))
            return resp
    else:
        return render_template('login.html')

