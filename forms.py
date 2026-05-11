from flask_wtf  import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, BooleanField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from datetime import date

class registerForm(FlaskForm):
    username = StringField('Usrename', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('sign up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('login')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=50)])
    description = TextAreaField('Description', validators=[Length(max=200)])
    priority = SelectField(
        'Priority',
        choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')],
        coerce=int,
        validators=[DataRequired()]
    )
    status = BooleanField('Completed')
    date = DateField(
        "Event Date",
        format='%Y-%m-%d', 
        validators=[DataRequired()],
        default=date.today  
    )
    submit = SubmitField('Save Task')