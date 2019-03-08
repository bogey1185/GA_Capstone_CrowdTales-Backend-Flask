from flask import jsonify, Blueprint, abort, make_response
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
import json
import models
from flask_cors import CORS

#define user response fields

membership_fields = {
  'id': fields.String,
  'user_id': fields.String,
  'story': fields.String
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

# class Story(Resource):
#   def __init__(self):
#     #initialize parser
#     self.reqparse = reqparse.RequestParser()
#     #add form of args to control requests
#     self.reqparse.add_argument(
#       'creator',
#       required=True,
#       help='No creator provided.', 
#       location=['form', 'json']
#     )
#     self.reqparse.add_argument(
#       'genre',
#       required=True,
#       help='No genre provided.', 
#       location=['form', 'json']
#     )
#     self.reqparse.add_argument(
#       'title',
#       required=True,
#       help='No title provided.', 
#       location=['form', 'json']
#     )
#     self.reqparse.add_argument(
#       'text',
#       required=True,
#       help='No text provided.', 
#       location=['form', 'json']
#     )
#     self.reqparse.add_argument(
#       'status',
#       required=False,
#       help='No status provided.', 
#       location=['form', 'json']
#     )
#     self.reqparse.add_argument(
#       'currentContrib',
#       required=False,
#       help='No contributor provided.', 
#       location=['form', 'json']
#     )
#     super().__init__

#   #get specific stories
#   @marshal_with(story_fields)
#   def get(self, id):
#     story = models.Story.get(models.Story.id == id)
#     return story

#   # edit story
#   @marshal_with(story_fields)
#   def put(self, id):
#     args = self.reqparse.parse_args()
#     edit = models.Story.update(**args).where(models.Story.id == id)
#     edit.execute()
#     #.update only returns the num of rows changed. so, if you want it
#     # to return the updated db entry, requery:
#     changed_story = models.Story.get(models.Story.id == id) #returns updated object
#     return change_story

#   def delete(self, id):
#     query = models.Story.delete().where(models.Story.id == id)
#     query.execute()
#     return 'resource deleted'

memberships_api = Blueprint('resources.memberships', __name__)
api = Api(memberships_api)

api.add_resource(
  MembershipList,
  '/members',
  endpoint='memberships'
)

# api.add_resource(
#   Story,
#   '/stories/<int:id>',
#   endpoint='story'
# )










