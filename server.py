import mysql.connector
from flask import Flask, request, jsonify, make_response
from werkzeug.security import check_password_hash
import jwt
import datetime
from functools import wraps
import json
from user import User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'


mydb = mysql.connector.connect(
    host="localhost",
    user="test",
    password="password",
    database="test"
)

mycursor = mydb.cursor()

# mycursor.execute("SHOW DATABASES")

# for x in mycursor:
    # print(x)


users = [
    User('test', 'test'),
    User('test1', 'test1'),
]


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None
        if 'Authorization' in request.headers:
            # if 'token' in request.headers or 'Authorization' in request.headers:
            if request.headers['Authorization'].split()[0] == 'Bearer':
                token = request.headers['Authorization'].split()[1]

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = next(
                (x for x in users if x.publicId == data['public_id']))

        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator


@app.route('/register', methods=['GET', 'POST'])
def signup_user():
    data = request.get_json()

    if data is None:
        return make_response('Username or password not provided', 400)

    print(data)

    if 'username' in data or 'password' in data:

        for user in users:
            if user.username == data['username']:
                return make_response('user already exists', 400)

        users.append(User(
            data['username'],
            data['password'])
        )

        return jsonify({'message': 'registered successfully'})
    return make_response('Username or password not provided', 400)


@app.route('/login', methods=['GET', 'POST'])
def login_user():

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
    try:
        user = next((x for x in users if x.username == auth.username), None)

        if user != None and check_password_hash(user.password, auth.password):
            token = jwt.encode({'public_id': user.publicId, 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

            return jsonify({'token': token.decode('utf-8')})
    except Exception as e:
        print('err')
        print(e)
        pass

    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route('/users', methods=['GET'])
def getUsers():
    return jsonify({'users': [x.toJSON() for x in users]})


@app.route('/user', methods=['GET'])
@token_required
def getUser(current_user):
    return jsonify({'user': current_user.toJSON()})


@app.route('/createHome', methods=['POST'])
@token_required
def createHome(current_user):
    addr = request.form.get('address')
    if addr is None:
        return make_response('Home address not specified', 400)

    current_user.addHome(addr)

    return jsonify({'message': 'home added successfully'})


@app.route('/homes', methods=['GET'])
@token_required
def homes(current_user):
    return jsonify({'address': current_user.homes})


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
