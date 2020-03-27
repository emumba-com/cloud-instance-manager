from flask import Flask, render_template, url_for, Blueprint, request
from .admin import *
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)

    return render_template('login.html')
