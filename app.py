# coding: utf-8

from flask import Flask, flash, url_for
from flask import render_template, request, redirect, g
from leancloud import LeanCloudError
from views.todos import todos_view
from flask.ext.login import LoginManager, current_user, login_user, logout_user, login_required
# from flask.ext.openid import OpenID
from leancloud import User, Query, Object


def get_user(uid):
    query = Query(Object.extend('User'))
    query.equal_to('objectId', uid)
    return query.find()[0] if query.count() else None


def is_authenticated():
    return True


def is_active():
    return True


def is_anonymous():
    return False


def get_id():
    return unicode('564c706460b2ed36206d0c47')


User.get_user = staticmethod(get_user)
User.is_authenticated = staticmethod(is_authenticated)
User.is_active = staticmethod(is_active)
User.is_anonymous = staticmethod(is_anonymous)
User.get_id = staticmethod(get_id)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# 动态路由
app.register_blueprint(todos_view, url_prefix='/todos')


@lm.user_loader
def load_user(uid):
    user = User()
    print(user.get_user(uid))
    return user.get_user(uid)


@app.route('/')
def index():
    return render_template('index.html')


@app.before_request
def before_request():
    g.user = current_user


@app.route('/new')
@login_required
def new():
    return 'ok'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        next_url = request.args.get('next') or '/'
        username = request.form.get('username')
        password = request.form.get('password')
        remember_me = False
        user = User()
        print next_url, username, password
        try:
            user.login(username, password)
            login_user(user, remember=remember_me)
            flash('Logged in successfully')
        except LeanCloudError:
            return redirect('/login')
        return redirect(next_url)
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        next_url = request.args.get('next') or '/'
        user = User()
        user.set('username', username)
        user.set('password', password)
        user.sign_up()
        flash('User successfully registered')
        return redirect(next_url)
    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    print g.user
    logout_user()
    print g.user
    return redirect(url_for('index'))
