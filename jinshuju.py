# coding: utf-8

import json
from uuid import uuid4

from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify

from sae import kvdb

app = Flask(__name__)
app.debug = True

db = kvdb.Client(debug=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form', methods=['GET'])
def form():
    key    = request.args.get('key', None)
    token  = request.args.get('token', None)
    target = request.args.get('target', None)

    if key and token and target:
        form = { 'key': key, 'token': token, 'target': target }
        return render_template('form.html', form=form)
    else:
        return render_template('error.html', message=u'无效的表单或推送地址')


@app.route('/entry', methods=['GET'])
def entry_get():
    filter = 'entry_%s_%s' % (request.args['key'], request.args['token'])
    entries = db.get_by_prefix(filter, limit=1)

    for entry in entries:
        return entry

    return 'null'

@app.route('/entry', methods=['DELETE'])
def entry_destroy():
    db.delete(request.args['entry_key'])

    return jsonify(success=True)

@app.route('/proxy/<token>', methods=['POST'])
def proxy(token):
    form = json.loads(request.data)
    key = form['form']

    print('Accept http-push on form', key, 'with token', token)

    entry_key = 'entry_%s_%s_%s' % (key, token, uuid4().hex)
    db.set(entry_key, request.data)

    return 'I got it. --- http://pushproxy.sinaapp.com/'