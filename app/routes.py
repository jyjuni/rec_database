import os
from app import app
from app.forms import LoginForm, AuthForm, SearchKeyForm, UpdateForm
from app.users import *
from app.retailers import *
from app.admin import *
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, flash
# from flask_login import login_required
# from flask_login import login_user, logout_user


# URI that connects to Part 2 database 
usr, pwd = "yj2682", "4749"
DATABASEURI = os.environ.get('DATABASE_URL') or f"postgresql://{usr}:{pwd}@35.196.192.139/proj1part2"
AUTH_TOKENS = ["yj2682"]
# SQLALCHEMY_TRACK_MODIFICATIONS = False

# creates a database engine that knows how to connect to the URI above.
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
    print("connecting")
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
    print("connection closing")
  except Exception as e:
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        form = LoginForm()
        if form.validate_on_submit():
            cursor = g.conn.execute(f"SELECT * FROM users where user_name LIKE '%%{form.username.data}%%' AND password LIKE '%%{form.password.data}%%'" )
            user_info = {}
            for result in cursor:
                user_info = {k:v for k,v in result.items() if k != "password"}
                break

            if user_info: #username-password found in table
                # get order history
                user_id = user_info['user_id']
                cursor = g.conn.execute(query_order_history(user_id))
                all_items = []
                for result in cursor:
                    all_items.append(list(result.values()))
                all_items_title = list(result.keys()) if result else []

                context = {"user_info":user_info, "all_items":all_items, "all_items_title":all_items_title}
                return render_template('user.html', title='user_info', **context)

            else: #not found in table
                return render_template('login.html', title='Sign In', form=form, error="Username-password combination not found!")

    return render_template('login.html', title='Sign In', form=form)


@app.route('/retailer_login', methods=['GET', 'POST'])
def retailer_login():
    if request.method == 'POST':
        form = LoginForm()
        if form.validate_on_submit():
            # flash('Login requested for user {}, remember_me={}'.format(
            #     form.username.data, form.remember_me.data))
            cursor = g.conn.execute(f"SELECT * FROM retailer WHERE retailer_name LIKE '%%{form.username.data}%%' AND password LIKE '%%{form.password.data}%%'" )
            user_check = None
            for result in cursor:
                user_check = result
                break

            if user_check: #username-password found in table
                user_id = user_check['retailer_id']
                # query retailer info
                cursor = g.conn.execute(query_retailer_info(user_id))
                for result in cursor:
                    user_info = {k:v for k,v in result.items()}
                    break

                # query items info
                cursor = g.conn.execute(query_items_info(user_id))
                all_items = []
                for result in cursor:
                    all_items.append(list(result.values()))
                all_items_title = list(result.keys()) if result else []

                # query ads info
                cursor = g.conn.execute(query_ads_info(user_id))
                all_ads = []
                for result in cursor:
                    all_ads.append(list(result.values()))
                all_ads_title = list(result.keys()) if result else []

                context = {"user_info":user_info, "all_items":all_items, "all_items_title":all_items_title, "all_ads":all_ads, "all_ads_title":all_ads_title}
                return render_template('retailer.html', title='retailer_info', **context)

            else: #not found in table
                return render_template('retailer_login.html', title='Sign In', form=form, error="Username-password combination not found!")

    return render_template('login.html', title='Sign In', form=form)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = AuthForm()
    if form.validate_on_submit():
        if form.token.data in AUTH_TOKENS:
            return redirect('/admin')
    return render_template('admin_login.html', title='Sign In', form=form)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = SearchKeyForm()
    if form.validate_on_submit():
        return render_template('admin.html', title='admin', form=form)
    return render_template('admin.html', title='admin', form=form)

@app.route('/')
@app.route('/index')
def index():    
  """
  request is a special object that Flask provides to access web request information:
  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)

  total = []
  cursor = g.conn.execute(
    "SELECT COUNT(DISTINCT user_id) FROM users UNION ALL SELECT COUNT(DISTINCT retailer_id) FROM retailer UNION ALL SELECT COUNT(DISTINCT order_id) FROM order_detail UNION ALL SELECT COUNT(DISTINCT item_id) FROM item")
  for result in cursor:
    total.append(result[0])

  
  context = {"total_user": total[0], "total_retailer":total[1], "total_order":total[2], "total_item":total[3]}
  return render_template("index.html", **context)