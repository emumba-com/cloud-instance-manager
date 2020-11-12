import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from settings import bcrypt, db
from models.user import User
from flask import make_response, Blueprint, render_template, request, redirect, url_for

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

user_obj = User()


@auth_bp.route('/')
def auth():
    return render_template('login.html')


@auth_bp.route('/signin', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            # get user from db
            user = db.session.query(User).filter(User.name == username).first()
            if user:
                auth_token = user_obj.encode_auth_token(user.id)
                if bcrypt.check_password_hash(user.password, password):
                    if user.admin:
                        resp = make_response(redirect(url_for('admin.get_admin')))
                        resp.set_cookie("auth_token", auth_token)
                        return resp
                    resp = make_response(redirect(url_for('user.user')))
                    resp.set_cookie("auth_token", auth_token)
                    return resp
                return redirect(url_for('auth.auth'))
            resp = make_response(redirect(url_for('auth.auth')))
            return resp
        except Exception as login_exception:
            print(login_exception)
            resp = make_response(redirect(url_for('auth.auth')))
            return resp
    return render_template('login.html')
