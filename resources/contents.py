from flask import jsonify, Blueprint, abort, make_response
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
import json
import models
from flask_cors import CORS

#define user response fields

content_fields = {
  'id': fields.String,
  'user_id': fields.String,
  'date': fields.DateTime,
  'text': fields.String,
  'story_id': fields.String
}

class ContentList(Resource):
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
      'text',
      required=True,
      help='No text provided.', 
      location=['form', 'json']
    )
    self.reqparse.add_argument(
      'story_id',
      required=True,
      help='No text provided.', 
      location=['form', 'json']
    )
    super().__init__

  #get all content
  def get(self):
    content = [marshal(content, content_fields) for content in models.Content.select()]
    return {'content': content}

  #create new story
  @marshal_with(content_fields)
  def post(self):
    args = self.reqparse.parse_args()
    new_content = models.Content.create(**args)
    return new_content

class Content(Resource):
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
      'text',
      required=True,
      help='No text provided.', 
      location=['form', 'json']
    )
    self.reqparse.add_argument(
      'story_id',
      required=True,
      help='No text provided.', 
      location=['form', 'json']
    )
    super().__init__

  #get specific stories
  @marshal_with(content_fields)
  def get(self, id):
    content = models.Content.get(models.Content.id == id)
    return content

  # edit story
  @marshal_with(content_fields)
  def put(self, id):
    args = self.reqparse.parse_args()
    edit = models.Content.update(**args).where(models.Content.id == id)
    edit.execute()
    #.update only returns the num of rows changed. so, if you want it
    # to return the updated db entry, requery:
    changed_content = models.Content.get(models.Content.id == id) #returns updated object
    return changed_content

  def delete(self, id):
    target = models.Content.get(models.Content.id == id)
    query = target.delete_instance(recursive=True)
    return 'resource deleted'

content_api = Blueprint('resources.contents', __name__)
api = Api(content_api)

api.add_resource(
  ContentList,
  '/content',
  endpoint='contents'
)

api.add_resource(
  Content,
  '/content/<int:id>',
  endpoint='content'
)










