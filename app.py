import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '.'))
from config import *

from flask import render_template

from settings import app, db

@app.route('/')
def index():
    return render_template('login.html')


# Importing blueprints
from auth import auth_bp
from admin import admin_bp
from user_blueprint import user_bp

# Registring blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    db.init_app(app)
    app.run()
