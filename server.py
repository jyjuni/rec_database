#!/usr/bin/env python

"""
Columbia's COMS W4111.003 Introduction to Databases
Webserver

To run locally:

    python server.py

Go to https://34.139.146.205:8111/ in your browser.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

# URI that connects to Part 2 database 
DATABASEURI = "postgresql://yj2682:4749@35.196.192.139/proj1part2"

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


@app.route('/')
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
  cursor.close()

  
  context = {"total_user": total[0], "total_retailer":total[1], "total_order":total[2], "total_item":total[3]}
  return render_template("index.html", **context)

@app.route('/user')
def user():
  return render_template("user.html")

@app.route('/retailer')
def retailer():
  return render_template("retailer.html")

@app.route('/admin')
def admin():
  return render_template("admin.html")


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click
  print("hi")
  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
