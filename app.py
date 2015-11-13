# coding: utf-8

from flask import Flask
from flask import render_template, request, redirect
from leancloud import LeanCloudError
from views.todos import todos_view
from models import Developer
import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID

app = Flask(__name__)

lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(os.path.dirname(__file__), 'tmp'))


# 动态路由
app.register_blueprint(todos_view, url_prefix='/todos')


@lm.user_loader
def load_user(uid):
    return Developer.get_user(uid)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if request.method == 'POST':
        next_url = request.args.get('next') or '/'
        username = request.form.get('username')
        password = request.form.get('password')
        user = Developer()
        oid.try_login()
        # try:
        #     user.login(username, password)
        # except LeanCloudError:
        #     return redirect('/login')
        # return redirect(next_url)
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        next_url = request.args.get('next') or '/'
        user = Developer()
        user.set('username', username)
        user.set('password', password)
        user.sign_up()
        return redirect(next_url)
    return render_template('signup.html')
