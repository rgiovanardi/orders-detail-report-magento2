from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User
from app.magento import get_mage_orders, get_mage_orders_with_name_filter, mage_get_all_order_ids, mage_group_all_order_details_important, mage_get_salable_quantity
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    mage_all_orders = get_mage_orders_with_name_filter('Menu')
    order_id_list = mage_get_all_order_ids(mage_all_orders)
    final_details_list = mage_group_all_order_details_important(order_id_list)
    salable_quantity_list = mage_get_salable_quantity()
    return render_template('index.html', title='Home', mage_all_orders = mage_all_orders, final_details_list = final_details_list, salable_quantity_list = salable_quantity_list)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))