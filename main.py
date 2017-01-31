#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
from flask import Flask, redirect, url_for, request, render_template, jsonify, flash, Response, g
import MySQLdb
from flaskext.mysql import MySQL
import sqlite3
from sqlalchemy import or_
import jinja2
from sql import session, engine
from models import Customer
from forms import CustomerForm

app = Flask(__name__)
app.secret_key = 'some_secret'

Customer.metadata.create_all(engine)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

#response in case of error
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# GET home
@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')

#GET all customers
@app.route('/customers', methods=['GET'])
def customers():
    customers = session.query(Customer).all()
    return render_template('index.html', customers=customers)

#GET customer by Id
@app.route("/customers/<int:c_id>", methods=['GET'])
def show_customer(c_id):
    cust = session.query(Customer).get(c_id)
    return render_template('one_cust.html', cust=cust)

#GET form for creating new customer
@app.route("/add", methods=['GET'])
def _add_customers():
    form = CustomerForm(request.form)
    return render_template('customer_form.html', form=form, method="POST", action="/add", error=None, submit_text="Save")

#POST new customer
@app.route("/add", methods=['POST'])
def add_customers():
    form = CustomerForm(request.form)
    error = None
    if form.validate():
        customer = Customer(form.first_name.data, form.last_name.data, form.email.data, form.age.data)
        flash('You sucessfully added a new customer!')
        session.add(customer)
        session.commit()
        return redirect(url_for('customers'))
    else:
        error = "Fields are not filled correctly!"
        return render_template('customer_form.html', form=form, method="POST", action="/add", error=error, submit_text="Save")

#GET customer to edit, by Id
@app.route("/customers/<int:c_id>/edit", methods=['GET'])
def showedit_customer(c_id):
    form = CustomerForm(request.form, session.query(Customer).get(c_id))
    return render_template('customer_form.html', form=form, method="POST", action="/customers/%s/edit" % c_id, submit_text="Save changes")

#POST edited customer
@app.route("/customers/<int:c_id>/edit", methods=['POST'])
def edit_customer(c_id):
    form = CustomerForm(request.form)
    if form.validate():
        cust_edited = Customer(form.first_name.data, form.last_name.data, form.email.data, form.age.data)
        flash('You sucessfully edited customer')
        customer_db = session.query(Customer).get(c_id)
        customer_db.first_name = cust_edited.first_name
        customer_db.last_name = cust_edited.last_name
        customer_db.age = cust_edited.age
        customer_db.email = cust_edited.email
        session.commit()
        return redirect(url_for('customers'))
    else:
        error = "Fields are not filled correctly!"
    return render_template('customer_form.html', form=form, method="POST", action="/customer/%s/edit" % c_id, submit_text="Save changes")

#delete customer
@app.route("/customers/<int:c_id>/delete", methods=['GET'])
def delete_customer(c_id):
    customer = session.query(Customer).get(c_id)
    session.delete(customer)
    session.commit()
    return redirect(url_for('customers'))

#GET customers by name/mail
@app.route("/search_name", methods=['GET'])
def search_name():
    q = request.values['q']
    customers = session.query(Customer).filter(
        or_(Customer.first_name.ilike("%" + q + "%"), Customer.last_name.ilike("%" + q + "%"), Customer.email.ilike("%" + q + "%"), Customer.age.ilike("%" + q + "%")))
    return render_template('search_results.html', customers=customers, q=q)

#GET customers by Id
@app.route("/search_id", methods=['GET'])
def search_id():
    idq = request.values['idq']
    customers = session.query(Customer).filter(Customer.c_id.like("%" + idq + "%"))
    return render_template('search_results.html', customers=customers, idq=idq)

#GET customers by age
@app.route("/search", methods=['GET'])
def search():
    param = request.values['param']
    customers = session.query(Customer).filter(Customer.age > param)
    return render_template('search_results.html', customers=customers, param=param)


if __name__ == "__main__":
    app.run()
