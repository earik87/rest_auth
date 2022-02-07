import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
auth = HTTPBasicAuth()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@auth.verify_password
def verify_password(username, password):
    # try to authenticate with username/password
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    password = request.json.get('password')

    if (username is None or firstname is None or
        lastname is None or password is None):
        return "Missing Arguments", 400

    if User.query.filter_by(username=username).first() is not None:
        return "Existing user, choose a different username", 400

    user = User(username=username,firstname=firstname,lastname=lastname)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({"username": user.username, 
                     "firstname": user.firstname,
                     "lastname": user.lastname}), 
            201)


@app.route('/api/resource', methods=['GET'])
@auth.login_required
def get_resource():
    return (jsonify({'data': 'Hello, %s!' % g.user.username}),
            201)


@app.route('/api/users/update', methods=['POST'])
@auth.login_required
def update_user():
    username = request.json.get('username')
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    password = request.json.get('password')

    if username is not None:
        if User.query.filter_by(username=username).first() is not None:
            return "Existing user, choose a different username", 400
        g.user.username = username
    if firstname is not None:
        g.user.firstname = firstname
    if lastname is not None:
        g.user.lastname = lastname
    if password is not None:
        g.user.hash_password(password)

    db.session.commit()
    return (jsonify({"data operation:": "update",
                     "username": g.user.username, 
                     "firstname": g.user.firstname,
                     "lastname": g.user.lastname}), 
            201)


@app.route('/api/users/delete', methods=['GET'])
@auth.login_required
def delete_user():
    db.session.delete(g.user)
    db.session.commit()
    return "The user is deleted!", 201
 

if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True)
