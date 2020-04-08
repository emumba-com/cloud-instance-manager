from .app import bcrypt, db
from .models.user import User
from flask import make_response, Blueprint, render_template, request, jsonify, redirect, url_for
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
user_obj = User()

@auth_bp.route('/')
def auth():
    return render_template('login.html')


@auth_bp.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = request.form.get('admin')
        print(admin, "admin checkbox")
        print(username, password)
        try:
            # get user from db
            user = db.session.query(User).filter(User.name == username).first()
            # TODO if condition for user existance
            if user:
                auth_token = user_obj.encode_auth_token(user.id)
                print(auth_token)
                print(user.admin, "are you admin")
                if bcrypt.check_password_hash(user.password, password):
                    print("password matches")
                    #TODO: Add generated token to cockies
                    if user.admin:
                        resp = make_response(redirect(url_for('admin.admin')))
                        resp.set_cookie("auth_token", auth_token)
                        return resp
                    resp = make_response(redirect(url_for('user.user')))
                    resp.set_cookie("auth_token", auth_token)
                    return resp
                else:
                    # password didn't matches
                    return redirect(url_for('auth.auth'))
            # TODO
            else:
                # need to generate new token for that user...
                resp = make_response(redirect(url_for('auth.auth')))
                return resp
        except Exception as e:
            # TODO: Add internal server error message incase of exception.
            print(e)
            resp = make_response(redirect(url_for('auth.auth')))
            return resp
    else:
        return render_template('login.html')

