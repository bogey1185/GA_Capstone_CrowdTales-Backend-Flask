from flask import jsonify, Blueprint, abort, make_response
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from playhouse.shortcuts import model_to_dict, dict_to_model
import json
import models
from flask_cors import CORS

#define user response fields

bookmark_fields = {
  'id': fields.String,
  'user_id': fields.String,
  'story_id': fields.String
}

bookmarkstory_fields = {
  'id': fields.String,
  'user_id': fields.String,
  'story_id': fields.String,
  'username': fields.String,
  'date': fields.String,
  'title': fields.String,
  'text': fields.String,
  'status': fields.String
}

class BookmarkList(Resource):
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

  #get all bookmarks
  def get(self):
    bookmarks = [marshal(bookmark, bookmark_fields) for bookmark in models.Bookmark.select()]
    return {'bookmarks': bookmarks}

  #create new bookmark
  @marshal_with(bookmark_fields)
  def post(self):
    args = self.reqparse.parse_args()
    new_bookmark = models.Bookmark.create(**args)
    return new_bookmark

class Bookmark(Resource):
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

  #get specific bookmark
  @marshal_with(bookmark_fields)
  def get(self, id):
    bookmark = models.Bookmark.get(models.Bookmark.id == id)
    return bookmark

  # edit story
  @marshal_with(bookmark_fields)
  def put(self, id):
    args = self.reqparse.parse_args()
    edit = models.Bookmark.update(**args).where(models.Bookmark.id == id)
    edit.execute()
    #.update only returns the num of rows changed. so, if you want it
    # to return the updated db entry, requery:
    changed_bookmark = models.Bookmark.get(models.Bookmark.id == id) #returns updated object
    return changed_bookmark

  #no recursive delete - just want to delete bookmark and nothing else
  def delete(self, id):
    query = models.Bookmark.delete().where(models.Bookmark.id == id)
    query.execute()
    return 'resource deleted'

class BookmarkStory(Resource):
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
    bookmarks = [bookmark for bookmark in models.Bookmark.select().where(models.Bookmark.user_id == id)]
    for bookmark in bookmarks:
      bookmark.username = model_to_dict(bookmark.story_id)['user_id']['username']
      bookmark.date = model_to_dict(bookmark.story_id)['date']
      bookmark.title = model_to_dict(bookmark.story_id)['title']
      bookmark.text = model_to_dict(bookmark.story_id)['text']
      bookmark.status = model_to_dict(bookmark.story_id)['status']

    jsonbookmarks = [marshal(bookmark, bookmarkstory_fields) for bookmark in bookmarks]
    return {'bookmarks': jsonbookmarks}

bookmarks_api = Blueprint('resources.bookmarks', __name__)
api = Api(bookmarks_api)

api.add_resource(
  BookmarkList,
  '/bookmarks',
  endpoint='bookmarks'
)

api.add_resource(
  Bookmark,
  '/bookmarks/<int:id>',
  endpoint='bookmark'
)

api.add_resource(
  BookmarkStory,
  '/bookmarkstory/<int:id>',
  endpoint='bookmarkstory'
)









