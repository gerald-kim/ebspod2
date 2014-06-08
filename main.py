import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'libs'))

from google.appengine.ext.webapp.util import run_wsgi_app
from flask import Flask
from flask.globals import *
from flask.templating import render_template
from model import *

app = Flask(__name__)

@app.route('/')
def index():
    programs = Program.all()
    return render_template("index.html", programs=programs)

@app.route('/programs/<key>')
def view_program(key):
    program = Program.get_by_key_name(key)
    episodes = Episode.all().filter('program = ', program).order('-title')

    server_url = request.environ['SERVER_NAME'] + ':' + request.environ['SERVER_PORT']

    if request.args.get('xml')!=None:
        return render_template('program.xml', program=program, episodes=episodes.fetch(30), server_url = server_url), 200, {"Content-Type":"text/xml"}

    return render_template('program.html', program=program, episodes=episodes.fetch(30), server_url = server_url)


@app.route('/episodes/', methods=['POST'])
def create_episode():
    if ClientKey.get_by_key_name(request.form['client_key']):
        Episode.create(request.form['program_name'], request.form['title'], request.form['file_url'])
        return "OK"
    else:
        return "ERROR-client key not found"

@app.route('/favicon.ico')
def favicon():
    return "Not found", 404

@app.route('/clients/create')
def create_client():
    ClientKey(key_name=request.args['client_key']).put()
    return "OK"

run_wsgi_app(app)
