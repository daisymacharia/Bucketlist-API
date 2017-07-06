import os.path
import sys
from inspect import getsourcefile

current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)
from flask_restful import Resource, abort
from flask import json, jsonify, request, g, Flask
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User, BucketListItems, BucketList
from instance.config import POSTS_PER_PAGE
from app.schema import UserRegisterSchema, UserLoginSchema, BucketListSchema

auth = HTTPTokenAuth()
app = Flask(__name__)


@auth.verify_token
# callback that Flask-HTTPAuth will use to verify the password for a
# specific user
def verify_user_token(token):
    verified_user = User.verify_auth_token(token)
    if type(verified_user) is not User:
        return False
    else:
        g.user = verified_user
        return True


class AuthResource(Resource):
    """"""
    method_decorators = [auth.login_required]


class UserRegister(Resource):
    """user registration"""
    def post(self):
        data = request.get_json()
        user_register_schema = UserRegisterSchema()
        errors = user_register_schema.validate(data)
        if errors:
            return errors
        fullnames = data['fullnames']
        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']

        if password != confirm_password:
            # verify that password and confirm password matches
            response = jsonify({'Error': 'Passwords do not match',
                                'status': 400})
            return response
        existing_email = User.query.filter_by(email=email).first()
        # verify email is not already in use
        if existing_email:
            response = jsonify({'Error': 'Email already in use',
                                'status': 409})
            return response
        new_user = User(fullnames=fullnames, email=email, password=password)
        new_user.add(new_user)
        new_user.hash_password(password)
        return jsonify({'message': 'User added successfully',
                        'status': 201})


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            response = jsonify({'Error': 'No data provided for registration',
                                'status': 400})
            return response
        user_login_schema = UserLoginSchema()
        errors = user_login_schema.validate(data)
        if errors:
            return errors
        email = data['email']
        password = data['password']
        email = User.query.filter_by(email=email).first()
        if not email:
            response = jsonify({'Error': 'Email not registered',
                                'status': 400})
            return response
        if email.verify_password(password):
            token = email.generate_auth_token()
            response = jsonify({'message': 'Login successful', 'status': 200,
                               'token': token.decode('ascii')})
            return response
        else:
            response = jsonify({'Error': 'Wrong password', 'status': 400})
            return response


class CreateBucketlist(AuthResource):
    def post(self):
        data = request.get_json()
        bucketlist_create = BucketListSchema()
        errors = bucketlist_create.validate(data)
        if errors:
            return errors
        name = data['name']
        existing_bucketlist = BucketList.query.filter_by(
            name=name, created_by=g.user.user_id).first()
        # verify name is not already in use
        if existing_bucketlist:
            response = jsonify({'Error': 'Bucketlist already created',
                                'status': 409})
            return response
        new_bucketlist_name = BucketList(name=name,
                                         created_by=g.user.user_id)
        new_bucketlist_name.add(new_bucketlist_name)
        response = jsonify({'Message': 'Bucketlist created successfully',
                            'status': 200})
        return response

    def get(self):
        bucketlist = BucketList.query.filter_by(created_by=g.user.user_id)
        if not bucketlist:
            response = jsonify({'Message': 'The user has no bucketlists',
                                'status': 404})
            return response
        bucketlist_get = BucketListSchema()
        return bucketlist_get.dump(bucketlist)


class BucketlistResource(AuthResource):

    def get(self, id):
        bucketlist = BucketList.query.filter_by(list_id=id).filter_by(
            created_by=g.user.user_id).first()
        if not bucketlist:
            response = jsonify({'Error': 'The bucketlist does not exist',
                                'status': 404})
            return response
        bucketlist_get = BucketListSchema()

        return bucketlist_get.dump(bucketlist)

    def put(self, id):
        bucketlist = BucketList.query.filter_by(list_id=id).filter_by(
            created_by=g.user.user_id).first()
        if not bucketlist:
            response = jsonify({'Error': 'The bucketlist does not exist',
                                'status': 404})
            return response
        data = request.get_json()
        bucketlist_update = BucketListSchema()
        validate_errors = bucketlist_update.validate(data)
        if validate_errors:
            return validate_errors
        name = data['name']
        existing_name = BucketList.query.filter_by(name=name).filter_by(
            created_by=g.user.user_id).first()
        if existing_name:
            response = jsonify(
                {'Error': 'Updating with same data not allowed',
                 'status': 409})
            return response
        bucketlist.name = data['name']
        bucketlist.update()
        response = jsonify(
            {'Message': 'Successfully updated bucketlist',
             'status': 200})
        return response

    def delete(self, id):
        bucketlist = BucketList.query.filter_by(list_id=id).filter_by(
            created_by=g.user.user_id).first()
        if not bucketlist:
            response = jsonify({'Error': 'The bucketlist does not exist',
                                'status': 404})
            return response
        bucketlist.delete(bucketlist)
        response = jsonify(
            {'Message': 'Successfully deleted bucketlist {}'.format(bucketlist.name),
             'status': 200})
        return response
