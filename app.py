from flask import Flask, request, abort, jsonify
from sqlalchemy import asc, desc
from datetime import datetime
from ConfigParser import ConfigParser
from os.path import join, expanduser

from models import db, Status, Tag

cnf = join(expanduser('~'), '.my.cnf')
cnf_parser = ConfigParser()
cnf_parser.read(cnf)
user = cnf_parser.get('client', 'user')
password = cnf_parser.get('client', 'password')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@localhost/trumptweets' % (user, password)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
db.init_app(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    return "Trump Tweets Web Service"


@app.route('/api/v1/status', methods=['GET'])
def status():
    return jsonify([x.as_dict() for x in
                    Status.query.order_by(desc(Status.created_at)).all()])


@app.route('/api/v1/tag', methods=['GET'])
def tag():
    return jsonify([x.as_dict() for x in Tag.query.all()])


if __name__ == '__main__':
    app.run(host="0.0.0.0")
