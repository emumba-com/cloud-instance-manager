from .admin import *
from .user import *
from .models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
user_obj = User()


@auth_bp.route('/')
def auth():
    return render_template('login.html')


@auth_bp.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # store them into database
        user_obj.addUser(username=username, password=password)
        print("User added successfuly")

        print(username, password)
        if username == "imtiaz1519" and password == "123":
            return redirect(url_for('admin.admin'))
        else:
            # fetch user's list from database and authenticate
            return redirect(url_for('user.user'))
    return render_template(url_for('auth'))
