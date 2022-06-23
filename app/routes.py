import os
from app import app
from app.forms import LoginForm, AuthForm, SearchKeyForm, UpdateForm, UpdateItemForm, DeleteItemForm
from app.users import *
from app.retailers import *
from app.admin import *
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, flash, url_for, session
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
    form = LoginForm()
    if form.validate_on_submit():
        cursor = g.conn.execute(f"SELECT user_id, user_name, TO_CHAR(created_time, 'yyyy-mm-dd') created_time, TO_CHAR(dob, 'yyyy-mm-dd') dob, gender FROM users where user_name LIKE '%%{form.username.data}%%' AND password LIKE '%%{form.password.data}%%'" )
        user_info = {}
        for result in cursor:
            user_info = {k:v for k,v in result.items()}
            break

        if form.submit.data: # login
            if user_info: #username-password found in table
                session['user_info'] = user_info
                return redirect(url_for("user", user_info=user_info))
            
            else: #not found in table
                return render_template('login.html', title='Sign In', form=form, error="Username-password combination not found!")
        elif form.signup.data: # signup
            if user_info: #username-password combination already exist
                return render_template('login.html', title='Sign In', form=form, error="Username-password combination already exists!")
            else: #register new user account
                # generate user_id
                cursor = g.conn.execute("SELECT MAX(user_id)+1 FROM users;")
                for result in cursor:
                    user_id = result[0]
                    break

                # insert new user
                cursor = g.conn.execute(query_insert_newuser(user_id, form.username.data, form.password.data))
                cursor = g.conn.execute(f"SELECT user_id, user_name, TO_CHAR(created_time, 'yyyy-mm-dd') created_time, TO_CHAR(dob, 'yyyy-mm-dd') dob, gender FROM users where user_name LIKE '%%{form.username.data}%%' AND password LIKE '%%{form.password.data}%%'" )
                user_info = {}
                for result in cursor:
                    user_info = {k:v for k,v in result.items()}
                    break
                
                assert(user_info)
                session['user_info'] = user_info

                return redirect(url_for("user", user_info=user_info))
                
    return render_template('login.html', title='Sign In', form=form)


@app.route('/user', methods=['GET', 'POST'])
def user():
    form = request.form
    user_info = session['user_info']
    # get order history
    user_id = user_info['user_id']
    print(user_info['dob'], user_info['created_time'], type(user_info['dob']))
    cursor = g.conn.execute(query_order_history(user_id))
    all_items = []
    for result in cursor:
        all_items.append(list(result.values()))
        break
    all_items_title = list(result.keys()) if all_items else []
    context = {"user_info":user_info, "all_items":all_items, "all_items_title":all_items_title}
    return render_template('user.html', title='user_info', **context, form=form)

    
@app.route('/update_user', methods=['GET', 'POST'])
def update_user():
    print('update user')

    form=UpdateForm()
    if form.validate_on_submit():
        cursor = g.conn.execute(f"UPDATE users SET user_name='{form.new_username.data}', password='{form.new_password.data}' WHERE user_name LIKE '%%{form.username.data}%%' AND password LIKE '%%{form.password.data}%%' RETURNING *;" )
        user_info = None
        for result in cursor:
            user_info = {k:v for k,v in result.items() if k != "password"}
            break

        if user_info: #username-password found in table
            print(user_info)            
            session['user_info'] = user_info
            return redirect(url_for("user", user_info=user_info))

        else: #not found in table
            return render_template('update.html', title='Sign In', form=form, error="Username-password combination already exists!")
    
    return render_template('update.html', title='update', form=form)

@app.route('/retailer_login', methods=['GET', 'POST'])
def retailer_login():
    form = LoginForm()
    if form.validate_on_submit():
        
        cursor = g.conn.execute(f"SELECT * FROM retailer WHERE retailer_name LIKE '%%{form.username.data}%%' AND password LIKE '%%{form.password.data}%%'" )
        user_check = None
        for result in cursor:
            user_check = result['retailer_id']
            break

        if form.submit.data: # login
            if user_check != None: #username-password found in table
                session['user_check'] = user_check
                return redirect(url_for("retailer", user_check=user_check))

            else: #not found in table
                return render_template('retailer_login.html', title='Sign In', form=form, error="Username-password combination not found!")
        
        elif form.signup.data: # signup
            if user_check != None:
                #username-password combination already exist
                return render_template('retailer_login.html', title='Sign In', form=form, error="Username-password combination already exists!")
            else: #register new retailer account
                # generate user_id
                cursor = g.conn.execute("SELECT MAX(retailer_id)+1 FROM retailer;")
                for result in cursor:
                    user_id = result[0]
                    break
                # insert new retailer
                cursor = g.conn.execute(query_insert_newretailer(user_id, form.username.data, form.password.data))
                session['user_check'] = user_id
                assert(user_id)
                return redirect(url_for("retailer", user_check=user_check))
                
    return render_template('retailer_login.html', title='Sign In', form=form)

@app.route('/retailer', methods=['GET', 'POST'])
def retailer():
    user_id = session['user_check']
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

@app.route('/update_retailer', methods=['GET', 'POST'])
def update_retailer():
    print('update retailer')
    form=UpdateForm()
    if form.validate_on_submit():
        cursor = g.conn.execute(f"UPDATE retailer SET retailer_name='{form.new_username.data}', password='{form.new_password.data}' WHERE retailer_name LIKE '%%{form.username.data}%%' AND password LIKE '%%{form.password.data}%%' RETURNING *;" )
        user_check = None
        for result in cursor:
            user_check = result['retailer_id']
            break

        if user_check is not None: #username-password found in table
            print(user_check)            
            session['user_check'] = user_check
            return redirect(url_for("retailer", user_check=user_check))

        else: #not found in table
            return render_template('update.html', title='Sign In', form=form, error="Username-password combination already exists!")
    
    return render_template('update.html', title='update', form=form)

@app.route('/update_item', methods=['GET', 'POST'])
def update_item():
    print('update item')
    form=UpdateItemForm()
    if form.validate_on_submit():
        print(form.item_id.data, form.item_name.data, form.price.data, form.brand.data, form.description.data, form.color.data)
        change_query = change_items_info(form.item_id.data, form.item_name.data, form.price.data, form.brand.data, form.description.data, form.color.data)
        cursor = g.conn.execute(change_query)
        user_check = None
        for result in cursor:
            user_check = {k:v for k,v in result.items() if k != "password"}
            break

        if user_check: #item found in table
            print(user_check)            
            session['user_check'] = user_check['retailer_id']
            return redirect(url_for("retailer", user_check=user_check))

        else: #not found in table
            return render_template('update_item.html', title='Sign In', form=form, error="Matching Item ID not found")
    
    return render_template('update_item.html', title='update', form=form)



@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = AuthForm()
    if form.validate_on_submit():
        if form.token.data in AUTH_TOKENS:
            return redirect('/admin')
    return render_template('admin_login.html', title='Sign In', form=form)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    print("hi admin")
    # show statistics
    total = []
    cursor = g.conn.execute(
        "SELECT COUNT(DISTINCT user_id) FROM users UNION ALL SELECT COUNT(DISTINCT retailer_id) FROM retailer UNION ALL SELECT COUNT(DISTINCT order_id) FROM order_detail UNION ALL SELECT COUNT(DISTINCT item_id) FROM item")
    for result in cursor:
        total.append(result[0])
    
    context = {"total_user": total[0], "total_retailer":total[1], "total_order":total[2], "total_item":total[3]}
    
    # search
    form = SearchKeyForm()
    if form.validate_on_submit():
        # query full info
        cursor = g.conn.execute(query_full_info(form.search_by.data, form.key.data))
        print(query_full_info(form.search_by.data, form.key.data))
        all_info = []
        for result in cursor:
            all_info.append(list(result.values()))

        if form.submit.data:

            if all_info:
                all_info_title = list(result.keys()) if result else []
                context["all_info"] = all_info
                context["all_info_title"] = all_info_title
                print(all_info)
                return render_template('admin.html', title='admin', form=form, **context)
            else:
                return render_template('admin.html', title='admin', form=form, error="Result not found", **context)

        elif form.delete.data:
            if all_info:
                all_info_title = list(result.keys()) if result else []
                session["all_info"] = all_info
                session["all_info_title"] = all_info_title
                # session["search_by"] = form.search_by.data
                # session["key"] = form.key.data
                print("redirecting to delete")
                return redirect(url_for('delete_item', all_info=all_info, all_info_title=all_info_title))
            else:
                return render_template('admin.html', title='admin', form=form, error="Cannot delete record that does not exist", **context)

    return render_template('admin.html', title='admin', form=form, **context)

@app.route('/delete_item', methods=['GET', 'POST'])
def delete_item():
    form = DeleteItemForm()
    all_info, all_info_title = session["all_info"], session["all_info_title"]
    if form.validate_on_submit():
        if form.delete.data:
            delete_query = query_delete_item(all_info_title[0], all_info[0][0])
            cursor = g.conn.execute(delete_query)
            return redirect(url_for('admin'))
        elif form.cancel.data:
            return redirect(url_for('admin'))


        
    context = {"all_info":all_info, "all_info_title":all_info_title}
    return render_template('delete_item.html', title='delete_item', form=form, **context)

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

  
  return render_template("index.html")