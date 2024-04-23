from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from webflask.models import User

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8)])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign up')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("the username is taken. please choose another one")
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("the email is taken. please choose another one")

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')

class UpdateUsernameForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    submit=SubmitField('Update Username')
            
class UpdateEmailForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('Update Email')

class PostForm(FlaskForm):
    title=StringField("Title",validators=[DataRequired(),Length(max=150)])
    text=TextAreaField("Content",validators=[DataRequired(),Length(max=1000)])
    private=BooleanField("Private")
    submit=SubmitField("Post")
    