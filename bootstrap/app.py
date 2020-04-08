from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from .config import *

app = Flask(__name__)
#
# app_settings = os.getenv(
#     'APP_SETTINGS',
#     'DevelopmentConfig'
#     #'project.server.config.DevelopmentConfig'
# )
# app.config.from_object(app_settings)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    # print())
    return render_template('login.html')


# Importing blueprints
from .auth import auth_bp
from .admin import admin_bp
from .user_blueprint import user_bp

# Registring blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    db.init_app(app)
    db.create_all()
    app.run(debug=True)
