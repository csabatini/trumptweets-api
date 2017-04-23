from flask import Flask, request, abort, jsonify
from sqlalchemy import asc, desc
from ConfigParser import ConfigParser
from os.path import join, expanduser
from datetime import datetime, timedelta
import uuid

from models import db, Status, UserProfile, StatusTag, TagCountMaxCreated

cnf = join(expanduser('~'), '.my.cnf')
cnf_parser = ConfigParser()
cnf_parser.read(cnf)
username = cnf_parser.get('client', 'user')
password = cnf_parser.get('client', 'password')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@localhost/trumptweets' % (username, password)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
db.init_app(app)


@app.route("/", methods=['GET'])
def index():
    return "Trump Tweets Web Service"


@app.route('/api/v1/status', methods=['GET'])
def status():
    results = Status.query
    filter_date = datetime.utcnow() - timedelta(days=1)
    if request.args is not None:
        if 'max_created_at' in request.args:
            filter_date = datetime.fromtimestamp(long(request.args['max_created_at']) / 1000.0)
        if 'tag_id' in request.args:
            filter_date = datetime.fromtimestamp(0)
            results = results.join(StatusTag, Status.status_id == StatusTag.status_id) \
                .filter(StatusTag.tag_id == request.args['tag_id'])
    return jsonify([x.as_dict() for x in
                    results
                   .filter(Status.created_at > filter_date)
                   .order_by(desc(Status.created_at))
                   .limit(100)
                   .all()])


@app.route('/api/v1/tag', methods=['GET'])
def tag():
    if request.args is None or 'id' not in request.args:
        return jsonify([x.as_dict() for x in TagCountMaxCreated.query.all()])
    else:
        return jsonify(TagCountMaxCreated.query
                       .filter_by(tag_id=request.args['id'])  # TODO: 400 on invalid id type
                       .first()
                       .as_dict())


@app.route('/api/v1/user', methods=['POST'])
def user_profile():
    payload = request.get_json()

    if payload['guid'] is None:
        user = \
            UserProfile(uuid.uuid4(), payload['push_enabled'], payload['device_token'])
        db.session.add(user)
    else:
        user = UserProfile.query.filter_by(guid=payload['guid']).first()
        token = payload['device_token']
        if token is not None:
            user.device_token = token
        user.push_enabled = payload['push_enabled']
    db.session.commit()
    return jsonify(user.as_dict())


@app.route('/api/v1/offset', methods=['POST'])
def offset():
    payload = request.get_json()
    if payload['user_profile']['guid'] is None:
        abort(400)
    elif payload['max_created_at'] == 0:
        return 'OK'

    user = UserProfile.query.filter_by(guid=payload['user_profile']['guid']).first()
    new_max_created_at = datetime.fromtimestamp(long(payload['max_created_at']) / 1000.0)

    if user.status_max_created_at is None or new_max_created_at > user.status_max_created_at:
        user.status_max_created_at = new_max_created_at
        db.session.commit()

    return 'OK'


if __name__ == '__main__':
    app.run(host="0.0.0.0")
