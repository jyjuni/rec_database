from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField, IntegerField, DateField
from wtforms.validators import DataRequired, NumberRange, Length, Optional
from datetime import date

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6), Length(min=6)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')
    signup = SubmitField('Sign Up')
    
class AuthForm(FlaskForm):
    token = StringField('Token', validators=[DataRequired()])
    submit = SubmitField('Log In')

class UserForm(FlaskForm):
    order = SubmitField('Order')
    update = SubmitField('Update')
    rate = SubmitField('Give a Rating')

class ShopForm(FlaskForm):
    search_by = SelectField('Search by', choices=[(1, 'item_id'), (2, 'item_name'), (3,'retailer'), (4, 'color'), (5,'brand')])
    key = StringField('Query', validators=[DataRequired()])
    submit = SubmitField('Search')

class OrderForm(FlaskForm):
    item_id = IntegerField('Item ID', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    order = SubmitField('Place Order')

class RateForm(FlaskForm):
    order_id = IntegerField('Order ID', validators=[DataRequired()])
    score = IntegerField('Score(0-5)', validators=[DataRequired(), NumberRange(min=0, max=5)])
    rate = SubmitField('Submit')

class UpdateForm(FlaskForm):
    username = StringField('Current Username', validators=[DataRequired()])
    password = PasswordField('Current Password', validators=[DataRequired(), Length(min=6)])
    new_username = StringField('New Username', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    update = SubmitField('Update')

class RetailerForm(FlaskForm):
    update_account = SubmitField('Update Account')
    update_item = SubmitField('Update Item')
    ads = SubmitField('Purchase Ads')

class AdsForm(FlaskForm):
    ad_title = StringField('Ad Title', validators=[DataRequired()])
    item_id = IntegerField('Item ID', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()],default=date.today)
    end_date = DateField('End Date', validators=[DataRequired()],default=date.today)
    order = SubmitField('Purchase')

    def validate_on_submit(self):
        result = super(AdsForm, self).validate()
        if (self.start_date.data>self.end_date.data) or (self.start_date.data < date.today()):
            return False
        else:
            return result

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
