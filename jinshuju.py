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

@app.route('/form/<form_id>', methods=['GET'])
def form(form_id):
    return render_template('form.html', form_id=form_id)

@app.route('/form/<form_id>', methods=['POST'])
def entry(form_id):
    filter = "entry_%s_" % form_id
    entries = get_by_prefix(filter, limit=1)

    for entry in entries:
        return entry

    return None

@app.route('/jinshuju/callback/<form_id>', methods=['POST'])
def callback(form_id):
    app.logger.info("Receiving data from form: %s", form_id)

    entry_id = uuid4().hex
    app.logger.info('  entry id: %s', entry_id)

    entry_key = 'entry_%s_%s' % (id, entry_id)
    db.set(entry_key, request.data)

    return 'I got it. --- http://pushproxy.sinaapp.com/'