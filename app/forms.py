from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, NumberRange, Length, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6), Length(min=6)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')
    signup = SubmitField('Sign Up')
    
class AuthForm(FlaskForm):
    token = StringField('Token', validators=[DataRequired()])
    submit = SubmitField('Log In')

# class ChangeForm(FlaskForm):
#     change = SubmitField('Change')

class UpdateForm(FlaskForm):
    username = StringField('Current Username', validators=[DataRequired()])
    password = PasswordField('Current Password', validators=[DataRequired(), Length(min=6)])
    new_username = StringField('New Username', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    update = SubmitField('Update')

class UpdateItemForm(FlaskForm):
    item_id = StringField('Item ID', validators=[DataRequired()])
    item_name = StringField('New Item Name')
    price = DecimalField('New Price', validators=[Optional(), NumberRange(min=0, max=9999)])
    brand = StringField('New Brand')
    description = StringField('New Description')
    color = StringField('New Color')
    update = SubmitField('Update')

class DeleteItemForm(FlaskForm):
    delete = SubmitField('Delete')
    cancel = SubmitField('Cancel')

class SearchKeyForm(FlaskForm):
    search_by = SelectField('Search by', choices=[(1, 'user_id'), (2, 'retailer_id'), (3, 'item_id'), (4,'order_id')])
    key = StringField('Query', validators=[DataRequired()])
    submit = SubmitField('Search')
    delete = SubmitField('Delete')
