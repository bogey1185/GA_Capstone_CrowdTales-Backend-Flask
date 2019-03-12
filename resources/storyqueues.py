from flask import jsonify, Blueprint, abort, make_response
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from playhouse.shortcuts import model_to_dict, dict_to_model
import json
import models
from flask_cors import CORS

#define user response fields

storyqueue_fields = {
  'id': fields.String,
  'user_id': fields.String,
  'story_id': fields.String
}

class StoryQueueList(Resource):
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

  #get all storyqueues
  def get(self):
    storyqueues = [marshal(storyqueue, storyqueue_fields) for storyqueue in models.StoryQueue.select()]
    return {'storyqueues': storyqueues}

  #create new storyqueue
  @marshal_with(storyqueue_fields)
  def post(self):
    args = self.reqparse.parse_args()
    new_storyqueue = models.StoryQueue.create(**args)
    return new_storyqueue

class StoryQueue(Resource):
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

  #get specific storyqueue
  @marshal_with(storyqueue_fields)
  def get(self, id):
    storyqueue = models.StoryQueue.get(models.StoryQueue.id == id)
    return storyqueue

  # edit story
  @marshal_with(storyqueue_fields)
  def put(self, id):
    args = self.reqparse.parse_args()
    edit = models.StoryQueue.update(**args).where(models.StoryQueue.id == id)
    edit.execute()
    #.update only returns the num of rows changed. so, if you want it
    # to return the updated db entry, requery:
    changed_storyqueue = models.StoryQueue.get(models.StoryQueue.id == id) #returns updated object
    return changed_storyqueue

  #no recursive delete here because we just want to remove 
  #the person who contributed from the queue. Don't want to 
  #delete anything they did.
  def delete(self, id):
    query = models.StoryQueue.delete().where(models.StoryQueue.id == id)
    query.execute()
    return 'resource deleted'

storyqueues_api = Blueprint('resources.storyqueues', __name__)
api = Api(storyqueues_api)

api.add_resource(
  StoryQueueList,
  '/storyqueues',
  endpoint='storyqueues'
)

api.add_resource(
  StoryQueue,
  '/storyqueues/<int:id>',
  endpoint='storyqueue'
)










