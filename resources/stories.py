from flask import jsonify, Blueprint, abort, make_response
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from playhouse.shortcuts import model_to_dict, dict_to_model
import json
import models
from flask_cors import CORS

#define user response fields

story_fields = {
  'id': fields.String,
  'user_id': fields.String,
  'date': fields.DateTime,
  'genre': fields.String,
  'title': fields.String,
  'text': fields.String,
  'status': fields.String,
  'currentContrib': fields.String,
  'username': fields.String
}

class StoryList(Resource):
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
    stories = [story for story in models.Story.select()]
    for story in stories:
      story.username = model_to_dict(story.user_id)['username']

    jsonstories = [marshal(story, story_fields) for story in stories]
    return {'stories': jsonstories}

  #create new story
  @marshal_with(story_fields)
  def post(self):
    args = self.reqparse.parse_args()
    new_story = models.Story.create(**args)
    return new_story  

class Story(Resource):
  def __init__(self):
    #initialize parser
    self.reqparse = reqparse.RequestParser()
    #add form of args to control requests
    self.reqparse.add_argument(
      'user_id',
      required=True,
      help='No user_id provided.', 
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
    self.reqparse.add_argument(
      'status',
      required=False,
      help='No status provided.', 
      location=['form', 'json']
    )
    self.reqparse.add_argument(
      'currentContrib',
      required=False,
      help='No contributor provided.', 
      location=['form', 'json']
    )
    super().__init__


  #get specific stories
  @marshal_with(story_fields)
  def get(self, id):
    story = models.Story.get(models.Story.id == id)
    return story

  # edit story
  @marshal_with(story_fields)
  def put(self, id):
    args = self.reqparse.parse_args()
    edit = models.Story.update(**args).where(models.Story.id == id)
    edit.execute()
    #.update only returns the num of rows changed. so, if you want it
    # to return the updated db entry, requery:
    changed_story = models.Story.get(models.Story.id == id) #returns updated object
    return changed_story

  def delete(self, id):
    target = models.Story.get(models.Story.id == id)
    query = target.delete_instance(recursive=True)
    return 'resource deleted'

class UserStory(Resource):
  def __init__(self):
    #initialize parser
    self.reqparse = reqparse.RequestParser()
    #add form of args to control requests
    self.reqparse.add_argument(
      'user_id',
      required=True,
      help='No user_id provided.', 
      location=['form', 'json']
    )
    super().__init__

  #get stories with specific user_id
  def get(self, id):
    stories = [marshal(story, story_fields) for story in models.Story.select().where(models.Story.user_id == id)]
    return {'stories': stories}

stories_api = Blueprint('resources.stories', __name__)
api = Api(stories_api)

api.add_resource(
  StoryList,
  '/stories',
  endpoint='stories'
)

api.add_resource(
  Story,
  '/stories/<int:id>',
  endpoint='story'
)

api.add_resource(
  UserStory,
  '/userstories/<int:id>',
  endpoint='userstory'
)









