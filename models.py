import os
import datetime
from peewee import *
from playhouse.db_url import connect
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

DATABASE = SqliteDatabase('crowdtalesdatabase.sqlite')

class User(UserMixin, Model):
  username      = CharField(unique=True)
  email         = CharField(unique=True)
  password      = CharField()

  class Meta:
    database = DATABASE

  @classmethod
  def create_user(cls, username, email, password):
    #sanitize email address
    email = email.lower()
    
    try: #see if user exists by querying email
      cls.select().where(cls.email == email).get() 
    
    except cls.DoesNotExist: #if user doesn't exist, create user
      user = cls(username=username, email=email)
      user.password = generate_password_hash(password)
      user.save()
      return user

    else: #if user does exist already
      raise Exception('Email address already in use.')

class Story(Model):
  creator         = ForeignKeyField(User, backref='user')
  date            = DateTimeField(default=datetime.datetime.now) 
  genre           = CharField()
  title           = CharField() 
  text            = TextField() #writing prompt
  status          = CharField(default='in prompt') #starts as inprompt. When first person adds content, it is chagned to 'inProgress'. Changes to vote complete when project just needs ending. chagnes to vote finish when ending is done. When complete, 'complete'
  currentContrib  = CharField() #current person with duty to contribute
 
  class Meta:
    database = DATABASE

class Content(Model):
  username  = ForeignKeyField(User, backref='user') 
  date      = DateTimeField(default=datetime.datetime.now)
  text      = TextField()
  votedate  = DateTimeField() 

  class Meta:
    database = DATABASE

class Membership(Model): # this model tracks stories where user has contributed
  user      = ForeignKeyField(User, backref='user')
  story     = ForeignKeyField(Story, backref='story')

  class Meta:
    database = DATABASE

class StoryQueue(Model): # this model tracks stories where user is queued to contribute
  user      = ForeignKeyField(User, backref='user')
  story     = ForeignKeyField(Story, backref='story')

  class Meta:
    database = DATABASE

class Bookmark(Model): #this model used to track stories that user wants to follow, but not contribute
  user      = ForeignKeyField(User, backref='user')
  story     = ForeignKeyField(Story, backref='story')

  class Meta:
    database = DATABASE

class Vote(Model):
  user      = ForeignKeyField(User, backref='user')
  vote      = CharField()
  content   = ForeignKeyField(Content, backref='content')

  class Meta:
    database = DATABASE

class Comment(Model): 
  user      = ForeignKeyField(User, backref='user')
  date      = DateTimeField(default=datetime.datetime.now)
  text      = TextField()
  content   = ForeignKeyField(Content, backref='content') #this key field will be used if the comment is assigned to a content submission
  comments  = ForeignKeyField('self') # this key field will be used if a comment is assigned to a comment

  class Meta:
    database = DATABASE

def initialize():
  DATABASE.connect()
  DATABASE.create_tables([User, Story, Content, Membership, StoryQueue, Bookmark, Vote, Comment], safe=True)
  DATABASE.close()

