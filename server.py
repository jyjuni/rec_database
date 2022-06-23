#!/usr/bin/env python

"""
Columbia's COMS W4111.003 Introduction to Databases
Webserver

To run locally:

    python server.py

Go to https://34.139.146.205:8111/ in your browser (external address is reserved to be static).
"""

from app import app

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

  