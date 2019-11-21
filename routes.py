from flask import Blueprint, render_template, flash, redirect, url_for, request, session, jsonify, json
from haystack_web import bcrypt, db, mysql
from haystack_web.models import User
from haystack_web.user.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('market.market_main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form, title='Sign Up')


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('market.market_main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('market.market_main'))
        else:
            flash(f'Login Unsuccessful. Please check your email and password', 'danger')
    return render_template('login.html', form=form, title='Log In')


@users.route("/logout")
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('home.index'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    trans = user_transaction(current_user.id)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pic/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form, trans=trans)


@users.route("/user_transaction")
def user_transaction(user_id):
    cur = mysql.connection.cursor()
    sql = 'select * from product as p join transaction as t on p.prod_id=t.prod_id where t.trans_username = %s'
    cur.execute(sql, [user_id])
    total = list(cur.fetchall())
    return total

