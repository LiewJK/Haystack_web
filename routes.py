from flask import Blueprint, request, render_template, redirect, url_for, session
from flask_paginate import get_page_parameter, Pagination
from haystack_web import mysql
from haystack_web.market.forms import PurchaseForm
from flask_login import login_required

market = Blueprint('market', __name__)


@market.route('/market_main')
@login_required
def market_main():
    #  pagination setup
    per_page = 3
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1)*per_page
    cur = mysql.connection.cursor()
    sql = 'select * from product'
    cur.execute(sql)
    total = list(cur.fetchall())
    sql = 'select * from product LIMIT %s OFFSET %s'
    cur.execute(sql, [per_page, offset])
    res = list(cur.fetchall())
    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(total), record_name='Product',
                            css_framework='bootstrap4')
    return render_template('market.html', data=res, pagination=pagination)
    # return 'Hello World and happy day! and I have added it from GitLab!'


@market.route('/market_purchase/<int:prod_id>', methods=['GET', 'POST'])
@login_required
def market_purchase(prod_id):
    form = PurchaseForm()
    cur = mysql.connection.cursor()
    sql = 'select * from product where prod_id = %s'
    cur.execute(sql, [prod_id])
    res = list(cur.fetchall())
    if form.validate_on_submit():
        session['purchase_form_data'] = {"prod_id": prod_id, "name": form.name.data, "email": form.email.data,
                                         "phone": form.phone.data,  "add1": form.add1.data, "add2": form.add2.data,
                                         "city": form.city.data, "state": form.state.data,
                                         "postcode": form.postcode.data}
        return redirect(url_for('payment.payment_billing'))
    return render_template('purchase.html', title='Checkout', data=res, form=form)
