from flask import jsonify, Blueprint, abort, make_response
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
import json
import models

#define user response fields

user_fields = {
  'id': fields.String,
  'username': fields.String
}

class UserList(Resource):
  def __init__(self):
    self.reqparse = reqparse.RequestParser()
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
      'verify_password',
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
    if args['password'] == args['verify_password']:
      ##create our user
      user = models.User.create_user(username = args['username'], email = args['email'], password = args['password'])
      login_user(user)
      return marshal(user, user_fields), 201
    return make_response(
      json.dumps({
        'error': 'Passwords do not match. Please try again.'
      }), 400
    )


users_api = Blueprint('resources.users', __name__)
api = Api(users_api)

api.add_resource(
  UserList,
  '/users',
  endpoint='users'
)
















