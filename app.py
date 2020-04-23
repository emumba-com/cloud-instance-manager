import os
import sys
from flask import render_template

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '.'))

from auth import auth_bp
from admin import admin_bp
from user_blueprint import user_bp
from settings import app, db

# Registaring blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)


@app.route('/')
def index():
    return render_template('login.html')


if __name__ == '__main__':
    db.init_app(app)
    app.run()
