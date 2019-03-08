from flask import jsonify, Blueprint, abort, make_response
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
import json
import models
from flask_cors import CORS

#define user response fields

user_fields = {
  'id': fields.String,
  'username': fields.String
}

class UserList(Resource):
  def __init__(self):
    #initialize parser
    self.reqparse = reqparse.RequestParser()
    #add form of args to control requests
    self.reqparse.add_argument(
      'username',
      required=True,
      help='No username provided.', 
      location=['form', 'json']
    )
    self.reqparse.add_argument(
      'email',
      required=True,
      help='No email provided.',
      location=['form', 'json']
    )
    self.reqparse.add_argument(
      'password',
      required=True,
      help='No password provided.'
    )
    self.reqparse.add_argument(
      'password2',
      required=True,
      help='No password verification provided.'
    )
    super().__init__

  #get all users
  def get(self):
    users = [marshal(user, user_fields) for user in models.User.select()]
    return {'users': users}

  #create user route
  def post(self):
    args = self.reqparse.parse_args()
    print(args, ' this is args in create')
    if args['password'] == args['password2']:
      ##create our user
      user = models.User.create_user(username = args['username'], email = args['email'], password = args['password'])
      login_user(user)
      return marshal(user, user_fields), 201
    return make_response(
      json.dumps({
        'error': 'Passwords do not match. Please try again.'
      }), 400
    )

class User(Resource):
  def __init__(self):
    #initialize parser
    self.reqparse = reqparse.RequestParser()
    #add form of args to control requests
    self.reqparse.add_argument(
      'username',
      required=True,
      help='No username provided.', 
      location=['form', 'json']
    )
    super().__init__

  #get specific user
  @marshal_with(user_fields)
  def get(self, id):
    user = models.User.get(models.User.id == id)
    return user

  # edit story
  @marshal_with(user_fields)
  def put(self, id):
    args = self.reqparse.parse_args()
    edit = models.User.update(**args).where(models.User.id == id)
    edit.execute()
    #.update only returns the num of rows changed. so, if you want it
    # to return the updated db entry, requery:
    changed_user = models.User.get(models.User.id == id) #returns updated object
    return changed_user

  def delete(self, id):
    query = models.User.delete().where(models.User.id == id)
    query.execute()
    return 'resource deleted'

class UserLogin(Resource):
  def __init__(self):
    #initialize parser
    self.reqparse = reqparse.RequestParser()
    #add form of args to control requests
    self.reqparse.add_argument(
      'username',
      required=True,
      help='No username provided.', 
      location=['form', 'json']
    )
    self.reqparse.add_argument(
      'password',
      required=True,
      help='No password provided.'
    )
    super().__init__

  #login route
  def post(self):
    #parse args into usable info
    args = self.reqparse.parse_args()
    print(args, ' this is args in login')
    try: 
      #try and find the submitted username in database
      user = models.User.get(models.User.username == args['username'])
    #if username is not found:
    except models.User.DoesNotExist:
      return make_response(
        json.dumps({
          'error': 'Username or password is incorrect. Please try again.'
        }), 400
      )
    else:
      #if username was found, check password. 
      if check_password_hash(user.password, args['password'] ):
        #if password is a match, login user
        login_user(user)
        return marshal(user, user_fields), 201
      else:
        return make_response(
          json.dumps({
            'error': 'Username or password is incorrect. Please try again.'
          }), 400
        )

users_api = Blueprint('resources.users', __name__)
api = Api(users_api)

api.add_resource(
  UserList,
  '/users',
  endpoint='users'
)

api.add_resource(
  User,
  '/users/<int:id>',
  endpoint='user'
)

api.add_resource(
  UserLogin,
  '/login',
  endpoint='login'
)


