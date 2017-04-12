from flask import Flask, request, abort, jsonify
from sqlalchemy import asc, desc
from ConfigParser import ConfigParser
from os.path import join, expanduser
from datetime import datetime, timedelta
import uuid

from models import db, Status, UserProfile, Tag

cnf = join(expanduser('~'), '.my.cnf')
cnf_parser = ConfigParser()
cnf_parser.read(cnf)
username = cnf_parser.get('client', 'user')
password = cnf_parser.get('client', 'password')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@localhost/trumptweets' % (username, password)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
db.init_app(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    return "Trump Tweets Web Service"


@app.route('/api/v1/status', methods=['GET'])
def status():
    payload = request.get_json()
    filter_date = \
        datetime.utcnow() - timedelta(days=1) if 'max_created_at' not in payload else payload['max_created_at']
    return jsonify([x.as_dict() for x in
                    Status.query
                   .filter_by(Status.created_at >= filter_date)
                   .order_by(desc(Status.created_at)).all()])


@app.route('/api/v1/tag', methods=['GET'])
def tag():
    return jsonify([x.as_dict() for x in Tag.query.all()])


@app.route('/api/v1/user', methods=['GET', 'POST'])
def user_profile():
    payload = request.get_json()

    if payload['guid'] is None:
        user = \
            UserProfile(uuid.uuid4(), payload['push_enabled'], payload['device_token'])
        db.session.add(user)
        db.session.commit()
    else:
        user = UserProfile.query.filter_by(guid=payload['guid']).first()
        token = payload['device_token']
        if token is not None and token != user.device_token:
            user.device_token = token
            db.session.commit()
    return jsonify(user.as_dict())


if __name__ == '__main__':
    app.run(host="0.0.0.0")
