from flask import jsonify, Blueprint, abort, make_response
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from playhouse.shortcuts import model_to_dict, dict_to_model
import json
import models
from flask_cors import CORS

#define user response fields

membership_fields = {
  'id': fields.String,
  'user_id': fields.String,
  'story_id': fields.String
}

membershipstory_fields = {
  'id': fields.String,
  'user_id': fields.String,
  'story_id': fields.String,
  'username': fields.String,
  'date': fields.String,
  'title': fields.String,
  'text': fields.String,
  'status': fields.String
}

class MembershipList(Resource):
  def __init__(self):
    #initialize parser
    self.reqparse = reqparse.RequestParser()
    #add form of args to control requests
    self.reqparse.add_argument(
      'user_id',
      required=True,
      help='No user id provided.', 
      location=['form', 'json']
    )
    self.reqparse.add_argument(
      'story_id',
      required=True,
      help='No story id provided.', 
      location=['form', 'json']
    )
    super().__init__

  #get all memberships
  def get(self):
    memberships = [marshal(membership, membership_fields) for membership in models.Membership.select()]
    return {'memberships': memberships}

  #create new membership
  @marshal_with(membership_fields)
  def post(self):
    args = self.reqparse.parse_args()
    new_membership = models.Membership.create(**args)
    return new_membership

class Membership(Resource):
  def __init__(self):
    #initialize parser
    self.reqparse = reqparse.RequestParser()
    #add form of args to control requests
    self.reqparse.add_argument(
      'user_id',
      required=True,
      help='No user id provided.', 
      location=['form', 'json']
    )
    self.reqparse.add_argument(
      'story_id',
      required=True,
      help='No story id provided.', 
      location=['form', 'json']
    )
    super().__init__

  #get specific membership
  @marshal_with(membership_fields)
  def get(self, id):
    membership = models.Membership.get(models.Membership.id == id)
    return membership

  # edit story
  @marshal_with(membership_fields)
  def put(self, id):
    args = self.reqparse.parse_args()
    edit = models.Membership.update(**args).where(models.Membership.id == id)
    edit.execute()
    #.update only returns the num of rows changed. so, if you want it
    # to return the updated db entry, requery:
    changed_membership = models.Membership.get(models.Membership.id == id) #returns updated object
    return changed_membership

  def delete(self, id):
    target = models.Membership.get(models.Membership.id == id)
    query = target.delete_instance(recursive=True)
    return 'resource deleted'

class MembershipStory(Resource):
  def __init__(self):
    #initialize parser
    self.reqparse = reqparse.RequestParser()
    #add form of args to control requests
    self.reqparse.add_argument(
      'user_id',
      required=True,
      help='No user id provided.', 
      location=['form', 'json']
    )
    super().__init__

  #get specific membership
  def get(self, id):
    memberships = [membership for membership in models.Membership.select().where(models.Membership.user_id == id)]
    for membership in memberships:
      membership.username = model_to_dict(membership.story_id)['user_id']['username']
      membership.date = model_to_dict(membership.story_id)['date']
      membership.title = model_to_dict(membership.story_id)['title']
      membership.text = model_to_dict(membership.story_id)['text']
      membership.status = model_to_dict(membership.story_id)['status']

    jsonmemberships = [marshal(membership, membershipstory_fields) for membership in memberships]
    return {'memberships': jsonmemberships}

memberships_api = Blueprint('resources.memberships', __name__)
api = Api(memberships_api)

api.add_resource(
  MembershipList,
  '/memberships',
  endpoint='memberships'
)

api.add_resource(
  Membership,
  '/memberships/<int:id>',
  endpoint='membership'
)

api.add_resource(
  MembershipStory,
  '/membershipstory/<int:id>',
  endpoint='membershipstory'
)










