from wtforms import Form, TextField, validators, ValidationError, IntegerField, StringField
from wtforms.validators import email
from sql import session
from models import Customer

def get_customer():
    return session.query(Customer).all()

class CustomerForm(Form):
    first_name = StringField('Name', [validators.Required("Name missing!"), validators.Length(min=2, max=20)])
    last_name =StringField('Surname', [validators.Required("Surname missing!"), validators.Length(min=2, max=20)])
    email = StringField('Email', [validators.Required("Email missing!"), email("This field requires a valid email address")])
    age = IntegerField('Age', [validators.Required("Age missing!")])
