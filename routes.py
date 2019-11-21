from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import login_required, current_user
from haystack_web import mysql
import datetime
import time

confirm = Blueprint('confirm', __name__)


@confirm.route('/purchase_confirm')
@login_required
def purchase_confirm():
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    pur_data = session['purchase_form_data']
    bil_data = session['bill_form_data']
    cur = mysql.connection.cursor()
    sql = '''INSERT INTO transaction ( trans_time, trans_username, prod_id, trans_name, trans_phone, trans_email,
            trans_add1, trans_add2, trans_city, trans_state, trans_postcode, trans_cc_no, trans_cc_holder, 
            trans_cc_expiry_month, trans_cc_expiry_year, trans_cc_cvv ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s)'''
    cur.execute(sql, [timestamp, current_user.id,  int(pur_data['prod_id']), pur_data['name'], pur_data['phone'],
                      pur_data['email'], pur_data['add1'], pur_data['add2'], pur_data['city'], pur_data['state'],
                      pur_data['postcode'], bil_data['cc_no'], bil_data['cc_holder'], bil_data['cc_exp_m'],
                      bil_data['cc_exp_y'], bil_data['cc_cvv_no']])
    mysql.connection.commit()
    cur = mysql.connection.cursor()
    sql = 'select * from product where prod_id = %s'
    cur.execute(sql, [pur_data['prod_id']])
    res = cur.fetchall()
    if session.get('purchase_form_data') and session.get('bill_form_data') is None:
        return redirect(url_for('market.market_main'))
    else:
        session.pop('purchase_form_data')
        session.pop('bill_form_data')
    return render_template('purchase_confirm.html', title="Purchase Confirmation", data=pur_data, bil_data=bil_data,
                           res=res)
