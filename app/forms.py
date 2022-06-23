from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')
    signup = SubmitField('Sign Up')
    
class AuthForm(FlaskForm):
    token = StringField('Token', validators=[DataRequired()])
    submit = SubmitField('Log In')

class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    update = SubmitField('Update')
    show = SubmitField('show')

class SearchKeyForm(FlaskForm):
    search_by = SelectField('Search by', choices=[(1, 'user_id'), (2, 'retailer_id'), (3, 'item_id'), (4,'order_id')])
    key = StringField('Query', validators=[DataRequired()])

    submit = SubmitField('Search')
