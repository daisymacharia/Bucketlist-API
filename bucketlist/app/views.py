import os.path
import sys
from inspect import getsourcefile

current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)
from flask_restful import Resource
from flask import jsonify, request, g, Flask, make_response
from flask_httpauth import HTTPTokenAuth
from app.models import User, BucketListItems, BucketList
from app.schema import UserRegisterSchema, UserLoginSchema, BucketListSchema,\
    ItemsSchema

auth = HTTPTokenAuth()
app = Flask(__name__)


@auth.verify_token
# callback that Flask-HTTPAuth will use to verify the password for a
# specific user
def verify_user_token(token):
    """function that verifies that the user accessing the private
        endpoints is an athenticated user"""
    verified_user = User.verify_auth_token(token)
    if type(verified_user) is not User:
        return False
    else:
        g.user = verified_user
        return True


class AuthResource(Resource):
    """subclass of flask_restful.Resource with auth.login_required.
       All the methods declared in a resource that uses the
       AuthRequiredResource will require authentication."""
    method_decorators = [auth.login_required]


class UserRegister(Resource):
    """user registration: Allows the user to register a new account """
    def post(self):
        """Allows the user to post data to the client for registration"""
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
        response = ({'message': 'User added successfully',
                    'status': 201})
        return response


class UserLogin(Resource):
    """   user login: Allows the user to login to an existing account and
          generate an auth token that the user will use to access private
          endpoints"""

    def post(self):
        """Allows the user to post data to the client for login"""
        data = request.get_json()
        if not data:
            response = jsonify({'Error': 'No data provided for registration',
                                'status': 400})
            return response
        user_login_schema = UserLoginSchema()
        # validate data fetched
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
    """Create bucketlist:
       Allows the user to create a new bucketlist,
       edit an existing bucketlist,
       get bucketlist by id and all the
       bucketlists by the logged in user,
       delete a bucketlist"""
    def post(self):
        """ POST method for creation of a new bucketlist"""
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
        response = jsonify({'Message': 'Bucketlist {} created successfully'
                            .format(new_bucketlist_name.list_id),
                            'status': 200})
        return response

    def get(self, id=None):
        """GET method for getting a bucketlist by id,
           getting all bucketlists,
           Searching for bucketlist by name"""
        if id:
            bucketlist = BucketList.query.filter_by(list_id=id).filter_by(
                created_by=g.user.user_id).first()
            if not bucketlist:
                response = jsonify({'Error': 'The bucketlist does not exist',
                                    'status': 404})
                return response
            bucketlist_get = BucketListSchema()
            # return serialized data in json
            return bucketlist_get.dump(bucketlist)
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=20, type=int)
        search = request.args.get("q", type=str)
        if search:
            bucketlists = BucketList.query.filter(
                BucketList.created_by == g.user.user_id,
                BucketList.name.ilike('%' + search + '%'))\
                .paginate(page, limit, False)

        else:
            bucketlists = BucketList.query.filter_by(
                created_by=g.user.user_id).paginate(page, limit, False)
        bucketlist_get_all = BucketListSchema()
        if bucketlists.has_next:
            next_page = request.url_root + 'api/v1.0/bucketlists' +\
                '?limit=' + str(limit) + \
                '&page=' + str(page + 1)
        else:
            next_page = 'None'
        if bucketlists.has_prev:
            prev_page = request.url_root + 'api/v1.0/bucketlists' +\
                '?limit=' + str(limit) + \
                '&page=' + str(page - 1)
        else:
            prev_page = 'None'
        result = []
        response = bucketlist_get_all.dump(bucketlists.items, many=True).data
        meta_data = {'meta_data': {'next_page': next_page,
                                   'previous_page': prev_page,
                                   'total_pages': bucketlists.pages}}
        result.append(response)
        result.append(meta_data)
        return (jsonify(result))

    def put(self, id):
        """PUT method for updating a bucketlist"""
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
                {'Error': 'Updating with same data not allowed'})
            return make_response(response, 409)
        bucketlist.name = data['name']
        bucketlist.update()
        response = jsonify(
            {'Message': 'Successfully updated bucketlist'})
        return make_response(response, 200)

    def delete(self, id):
        """Delete method that deletes a specific bucketlist"""
        bucketlist = BucketList.query.filter_by(list_id=id).filter_by(
            created_by=g.user.user_id).first()
        if not bucketlist:
            response = jsonify({'Error': 'The bucketlist does not exist',
                                'status': 404})
            return response
        bucketlist.delete(bucketlist)
        response = jsonify(
            {'Message': 'Successfully deleted bucketlist {}'.format(
                bucketlist.name),
             'status': 200})
        return response


class BucketlistItems(AuthResource):
    """Bucketlistitems:
       Allows the user to create a new bucketlist item,
       edit an existing bucketlist item,
       get items by id and all the
       items by the logged in user,
       delete a bucketlist item"""

    def post(self, id):
        """POST method that allows the user to post dat for creation of a
           new bucketlist item
           Post data is validated and deserialized to json format"""
        bucketlist_creator = BucketList.query.filter_by(
            created_by=g.user.user_id).filter_by(list_id=id)
        if bucketlist_creator:
            data = request.get_json()
            item_create = ItemsSchema()
            errors = item_create.validate(data)
            if errors:
                return errors
            name = data['name']
            existing_item = BucketListItems.query.filter_by(
                name=name, bucketlist_id=id).first()
            # verify name is not already in use
            if existing_item:
                response = jsonify({'Error': 'Item already created',
                                    'status': 409})
                return response
            new_item = BucketListItems(name=name, bucketlist_id=id)
            new_item.add(new_item)
            response = jsonify({'Message': 'Item {} created successfully'
                               .format(new_item.name)})
            return make_response(response, 201)
        else:
            return jsonify({'error': 'Unauthorized access',
                            'status': 401})

    def put(self, id, item_id):
        """PUT method that allows the user to edit an existing
           bucketlist item"""

        bucketlist_creator = BucketList.query.filter_by(
            created_by=g.user.user_id).filter_by(list_id=id)
        item_update = ItemsSchema()
        data = request.get_json()
        validate_errors = item_update.validate(data, partial=True)
        if validate_errors:
            return validate_errors
        if bucketlist_creator:
            item = BucketListItems.query.filter_by(
                bucketlist_id=id).filter_by(item_id=item_id).first()
            if item:
                if 'done' in data:
                    done = data['done']
                    item.done = done
                elif 'name' in data:
                    name = data['name']
                    existing_name = BucketListItems.query.filter_by(
                        name=name).first()
                    if existing_name:
                        response = jsonify(
                            {'Error': 'Updating with same data not allowed'})
                        return make_response(response, 409)
                    item.name = name
                item.update()
                return jsonify({'message': 'Successfully updated item',
                                'status': 200})
            else:
                return jsonify({'error': 'Item not found',
                                'status': 400})
        return jsonify({'error': 'Unauthorized access',
                        'status': 401})

    def get(self, id, item_id=None):
        """GET method for getting a bucketlist item by id,
           getting all bucketlists items,
           Searching for bucketlist items by name"""
        bucketlist = BucketList.query.filter_by(list_id=id).filter_by(
            created_by=g.user.user_id).first()
        if bucketlist:
            if item_id:
                bucketlistitem = BucketListItems.query.filter_by(
                    item_id=item_id).filter_by(bucketlist_id=id)
                if not bucketlistitem:
                    response = jsonify({'Error': 'The bucketlist item' + " " +
                                        'does not exist', 'status': 404})
                    return response
                bucketlistitem_get = ItemsSchema()
                # return serialized data in json
                return bucketlistitem_get.dump(bucketlistitem, many=True).data
            page = request.args.get("page", default=1, type=int)
            limit = request.args.get("limit", default=20, type=int)
            search = request.args.get("q", type=str)
            if search:
                items = BucketListItems.query.filter(
                    BucketListItems.bucketlist_id == id,
                    BucketListItems.name.ilike('%' + search + '%'))\
                    .paginate(page, limit, False)

            else:
                items = BucketListItems.query.filter_by(
                    bucketlist_id=id).paginate(page, limit, False)
            items_get_all = ItemsSchema()
            if items.has_next:
                next_page = request.url_root + 'api/v1.0/bucketlists' +\
                    "/" + str(id) + '/items' + '?limit=' + str(limit) + \
                    '&page=' + str(page + 1)
            else:
                next_page = 'None'
            if items.has_prev:
                prev_page = request.url_root + 'api/v1.0/bucketlists' +\
                    "/" + str(id) + '/items' + '?limit=' + str(limit) + \
                    '&page=' + str(page - 1)
            else:
                prev_page = 'None'
            result = []
            response = items_get_all.dump(items.items, many=True).data
            meta_data = {'meta_data': {'next_page': next_page,
                                       'previous_page': prev_page,
                                       'total_pages': items.pages}}
            result.append(response)
            result.append(meta_data)
            return (jsonify(result))
        return jsonify({'error': 'Unauthorized access',
                        'status': 401})

    def delete(self, id, item_id):
        """Delete method that deletes a specific bucketlist"""
        bucketlist = BucketList.query.filter_by(list_id=id).filter_by(
            created_by=g.user.user_id).first()
        if bucketlist:
            bucketlistitem = BucketListItems.query.filter_by(
                item_id=item_id).filter_by(
                bucketlist_id=id).first()
            if not bucketlistitem:
                response = jsonify({'Error': 'The bucketlist item' + " " +
                                    'does not exist', 'status': 404})
                return response
            bucketlistitem.delete(bucketlistitem)
            response = jsonify(
                {'Message': 'Successfully deleted bucketlist'
                 " " + 'item {}'.format(bucketlistitem.name),
                 'status': 200})
            return response
        else:
            return jsonify({'Message': 'Bucketlist not found',
                            'status': 404})
