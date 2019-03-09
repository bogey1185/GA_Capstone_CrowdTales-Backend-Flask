from flask import jsonify, Blueprint, abort, make_response
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
import json
import models
from flask_cors import CORS

#define user response fields

comment_fields = {
  'id': fields.String,
  'user_id': fields.String,
  'date': fields.DateTime,
  'text': fields.String,
  'content_id': fields.String,
  'comment_id': fields.String
}

class CommentList(Resource):
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
      'content_id',
      help='No text provided.', 
      location=['form', 'json']
    )
    self.reqparse.add_argument(
      'comment_id',
      help='No text provided.', 
      location=['form', 'json']
    )
    super().__init__

  #get all content
  def get(self):
    comments = [marshal(comment, comment_fields) for comment in models.Comment.select()]
    return {'comments': comments}

 #create new content comment 
  @marshal_with(comment_fields)
  def post(self):
    args = self.reqparse.parse_args()
    new_comment = models.Comment.create(**args)
    return new_comment

class Comment(Resource):
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
      'content_id',
      help='No text provided.', 
      location=['form', 'json']
    )
    self.reqparse.add_argument(
      'comment_id',
      help='No text provided.', 
      location=['form', 'json']
    )
    super().__init__

  #get specific stories
  @marshal_with(comment_fields)
  def get(self, id):
    comment = models.Comment.get(models.Comment.id == id)
    return comment

  # edit story
  @marshal_with(comment_fields)
  def put(self, id):
    args = self.reqparse.parse_args()
    edit = models.Comment.update(**args).where(models.Comment.id == id)
    edit.execute()
    #.update only returns the num of rows changed. so, if you want it
    # to return the updated db entry, requery:
    changed_comment = models.Comment.get(models.Comment.id == id) #returns updated object
    return changed_comment

  def delete(self, id):
    target = models.Comment.get(models.Comment.id == id)
    query = target.delete_instance(recursive=True)
    return 'resource deleted'

comment_api = Blueprint('resources.comments', __name__)
api = Api(comment_api)

api.add_resource(
  CommentList,
  '/comments',
  endpoint='comments'
)

api.add_resource(
  Comment,
  '/comments/<int:id>',
  endpoint='comment'
)



