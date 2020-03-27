from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def index():
    # user_instance = User()
    # user_instance.addUser("User2", "test123")
    return render_template('login.html')


# Importing blueprints
from .auth import auth_bp
from .admin import admin_bp
from .user import user_bp

# Registring blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    db.init_app(app)
    db.create_all()
    app.run(debug=True)
