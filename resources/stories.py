from flask import jsonify, Blueprint, abort, make_response
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
import json
import models
from flask_cors import CORS

#define user response fields

story_fields = {
  'id': fields.String,
  'creator': fields.String,
  'date': fields.DateTime,
  'genre': fields.String,
  'title': fields.String,
  'text': fields.String,
  'status': fields.String,
  'currentContrib': fields.String
}

class StoryList(Resource):
  def __init__(self):
    #initialize parser
    self.reqparse = reqparse.RequestParser()
    #add form of args to control requests
    self.reqparse.add_argument(
      'creator',
      required=True,
      help='No creator provided.', 
      location=['form', 'json']
    )
    self.reqparse.add_argument(
      'genre',
      required=True,
      help='No genre provided.', 
      location=['form', 'json']
    )
    self.reqparse.add_argument(
      'title',
      required=True,
      help='No title provided.', 
      location=['form', 'json']
    )
    self.reqparse.add_argument(
      'text',
      required=True,
      help='No text provided.', 
      location=['form', 'json']
    )
    super().__init__

  #get all stories
  def get(self):
    stories = [marshal(story, story_fields) for story in models.Story.select()]
    return {'stories': stories}

  #create new story
  @marshal_with(story_fields)
  def post(self):
    args = self.reqparse.parse_args()
    print(args, ' this is args in create')
    new_story = models.Story.create(**args)
    return new_story


stories_api = Blueprint('resources.stories', __name__)
api = Api(stories_api)

api.add_resource(
  StoryList,
  '/stories',
  endpoint='stories'
)










