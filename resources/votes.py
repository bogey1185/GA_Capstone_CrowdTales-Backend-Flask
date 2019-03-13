from flask import jsonify, Blueprint, abort, make_response
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from playhouse.shortcuts import model_to_dict, dict_to_model
import json
import models
from flask_cors import CORS

#define user response fields
 
vote_fields = {
  'id': fields.String,
  'user_id': fields.String,
  'content_id': fields.String,
  'vote': fields.Integer
}

class VoteList(Resource):
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
      'content_id',
      required=True,
      help='No content id provided.', 
      location=['form', 'json']
    )
    self.reqparse.add_argument(
      'vote',
      required=True,
      help='No vote value provided.', 
      location=['form', 'json']
    )
    super().__init__

  #get all votes
  def get(self):
    votes = [marshal(vote, vote_fields) for vote in models.Vote.select()]
    return {'votes': votes}

  #create new vote
  @marshal_with(vote_fields)
  def post(self):
    args = self.reqparse.parse_args()
    new_vote = models.Vote.create(**args)
    return new_vote

class Vote(Resource):
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
      'content_id',
      required=True,
      help='No content id provided.', 
      location=['form', 'json']
    )
    self.reqparse.add_argument(
      'vote',
      required=True,
      help='No vote value provided.', 
      location=['form', 'json']
    )
    super().__init__

  #get specific vote
  @marshal_with(vote_fields)
  def get(self, id):
    vote = models.Vote.get(models.Vote.id == id)
    return vote

  # edit story
  @marshal_with(vote_fields)
  def put(self, id):
    args = self.reqparse.parse_args()
    edit = models.Vote.update(**args).where(models.Vote.id == id)
    edit.execute()
    #.update only returns the num of rows changed. so, if you want it
    # to return the updated db entry, requery:
    changed_vote = models.Vote.get(models.Vote.id == id) #returns updated object
    return changed_vote

  #no recursive delete - just want to delete vote and nothing else
  def delete(self, id):
    query = models.Vote.delete().where(models.Vote.id == id)
    query.execute()
    return 'resource deleted'

votes_api = Blueprint('resources.votes', __name__)
api = Api(votes_api)

api.add_resource(
  VoteList,
  '/votes',
  endpoint='votes'
)

api.add_resource(
  Vote,
  '/votes/<int:id>',
  endpoint='vote'
)










