import json
from uuid import uuid4

from flask import Flask
from flask import request
from flask import render_template

from sae import kvdb

app = Flask(__name__)
app.debug = True

db = kvdb.Client(debug=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form/', methods=['GET'])
def form():
    return render_template('form.html', form_id=form_id)

@app.route('/entry/', methods=['GET'])
def entry():
    filter = 'entry_%s_%s' % (request.args['key'], request.args['token'])
    entries = get_by_prefix(filter, limit=1)

    for entry in entries:
        return entry

    return None

@app.route('/proxy/<token>', methods=['POST'])
def proxy(token):
    form = json.loads(request.data)
    key = form['form']

    print('Accept http-push on form', key, 'with token', token)

    entry_key = 'entry_%s_%s_%s' % (key, token, uuid4().hex)
    db.set(entry_key, request.data)

    return 'I got it. --- http://pushproxy.sinaapp.com/'