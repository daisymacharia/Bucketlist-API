import os.path
import sys
from inspect import getsourcefile

current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)
from flask_restful import Resource, abort
from flask import json, jsonify, request, g
from app.models import User, BucketListItems, BucketList
from app.schema import UserRegisterSchema


class UserRegister(Resource):
    """user registration"""
    def post(self):
        data = request.get_json()
        if not data:
            response = jsonify({'Error': 'No data provided for registration',
                                'status': 400})
            return response
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
