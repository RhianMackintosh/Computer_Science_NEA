from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextField, IntegerField, SelectField, RadioField
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired, Length

#creates a form for the log in
class logInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])   #so the username must be 2-20 characters
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)]) #the password must be the same
    submit = SubmitField('Log in') #this submits the form

#creates the form for the contact
class ContactForm(FlaskForm):
    name = StringField("Name Of Student", [validators.DataRequired("Please enter your name.")])
    Gender = RadioField('Gender', choices=[('M', 'Male'), ('F', 'Female')])
    Address = StringField("Address")

    email = StringField("Email", [validators.DataRequired("Please enter your email address."),
                                validators.Email("Please enter your email address.")])

    Age = IntegerField("age")
    language = SelectField('Languages', choices=[('cpp', 'C++'),
                                                 ('py', 'Python')])
    submit = SubmitField("Send")

class SettingForm(FlaskForm):
    fname = StringField("First Name")
    sname = StringField("Surname")
    title = SelectField("Title", choices=[("miss","Miss"),("mr","Mr"),("ms","Ms"),("mrs","Mrs")])
    knownas = StringField("Known as name")

    save = SubmitField("Save")

class SignUpForm(FlaskForm):
    uname = StringField("Username", [validators.DataRequired()])
    fname = StringField("First Name", [validators.DataRequired()])
    sname = StringField("Surname", [validators.DataRequired()])
    title = SelectField("Title",[validators.DataRequired()])
    knownas = StringField("Known as name",[validators.DataRequired()])
    securityq = SelectField("SecuirtyQuestion",[validators.DataRequired()])
    securitya = StringField("Security Answer",[validators.DataRequired()])
    password = StringField("Password",[validators.DataRequired()])
    confirm = StringField("Confirm Password",[validators.DataRequired()])
    signupbutton = SubmitField("Sign Up",[validators.DataRequired()])