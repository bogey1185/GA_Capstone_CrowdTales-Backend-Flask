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
# class Story(Model):
#   creator         = ForeignKeyField(User, backref='user')
#   date            = DateTimeField(default=datetime.datetime.now) 
#   genre           = CharField()
#   title           = CharField() 
#   text            = TextField() #writing prompt
#   status          = CharField() #starts as inprompt. When first person adds content, it is chagned to 'inProgress'. Changes to vote complete when project just needs ending. chagnes to vote finish when ending is done. When complete, 'complete'
#   currentContrib  = CharField() 

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
      'date',
      required=False,
      help='No date provided.', 
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
      required=True,
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

  #get all stories
  def get(self):
    stories = [marshal(story, story_fields) for story in models.Story.select()]
    return {'stories': stories}

  # #create user route
  # def post(self):
  #   args = self.reqparse.parse_args()
  #   print(args, ' this is args in create')
  #   if args['password'] == args['password2']:
  #     ##create our user
  #     user = models.User.create_user(username = args['username'], email = args['email'], password = args['password'])
  #     login_user(user)
  #     return marshal(user, user_fields), 201
  #   return make_response(
  #     json.dumps({
  #       'error': 'Passwords do not match. Please try again.'
  #     }), 400
  #   )

stories_api = Blueprint('resources.stories', __name__)
api = Api(stories_api)

api.add_resource(
  StoryList,
  '/stories',
  endpoint='stories'
)










