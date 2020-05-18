import os
import sys
import time
from multiprocessing import Process
from datetime import datetime
from flask import render_template

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '.'))

from auth import auth_bp
from admin import admin_bp, fetch_instances_cost_from_aws
from user_blueprint import user_bp
from settings import app, db

# Registaring blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)


@app.route('/')
def index():
    return render_template('login.html')


def fetch_bill_from_aws(duration=86400):
    while True:
        fetch_instances_cost_from_aws()
        delay = duration + int(time.time() / duration) * duration - time.time()
        print("Going to sleep for %s seconds" % delay)
        time.sleep(delay)


def bill_scheduler():
    process = Process(target=fetch_bill_from_aws, args=(86400, ))
    process.start()


bill_scheduler()

if __name__ == '__main__':
    db.init_app(app)
    app.run()
