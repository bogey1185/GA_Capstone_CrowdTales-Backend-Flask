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
  stories       = ForeignKeyField(Story, backref='stories')
  memberships   = ForeignKeyField(Membership, backref='membership')
  bookmarks     = ForeignKeyField(Bookmarks, backref='bookmarks')

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
  username:       = ForeignKeyField(User, backref='user')
  date            = DateTimeField(default=datetime.datetime.now) 
  genre           = CharField()
  title           = CharField() 
  text            = TextField() #writing prompt
  membership      = ForeignKeyField(Membership, backref='membership') #list if people who contributed
  status          = CharField() #starts as inprompt. When first person adds content, it is chagned to 'inProgress'. Changes to vote complete when project just needs ending. chagnes to vote finish when ending is done. When complete, 'complete'
  queue           = ForeignKeyField(StoryQueue, backref='queue')
  currentContrib  = CharField() #current person with duty to contribute
  content         = ForeignKeyField(Content, backref='content')
 
  class Meta:
    database = DATABASE

class Content(Model):
  username  = ForeignKeyField(User, backref='user') 
  date      = DateTimeField(default=datetime.datetime.now)
  text      = TextField()
  votes     = ForeignKeyField(Vote, backref='vote')
  comments  = ForeignKeyField(Comment, backref='comment')
  votedate  = DateTimeField() 

  class Meta:
    database = DATABASE

class Membership(Model): # this model tracks stories where user has contributed
  username  = ForeignKeyField(User, backref='user')
  story     = ForeignKeyField(Story, backref='story')

  class Meta:
    database = DATABASE

class StoryQueue(Model): # this model tracks stories where user is queued to contribute
  username  = ForeignKeyField(User, backref='user')
  story     = ForeignKeyField(Story, backref='story')

  class Meta:
    database = DATABASE

class Bookmark(Model): #this model used to track stories that user wants to follow, but not contribute
  username  = ForeignKeyField(User, backref='user')
  story     = ForeignKeyField(Story, backref='story')

  class Meta:
    database = DATABASE

class Vote(Model):
  username  = ForeignKeyField(User, backref='user')
  vote      = CharField()
  content   = ForeignKeyField(Content, backref='content')

  class Meta:
    database = DATABASE

class Comment(Model): 
  username  = ForeignKeyField(User, backref='user')
  date      = DateTimeField(default=datetime.datetime.now)
  text      = TextField()
  comments  = ForeignKeyField('self')

  class Meta:
    database = DATABASE

def initialize():
  DATABASE.connect()
  DATABASE.create_tables([User, Story, Content, Membership, StoryQueue, Bookmark, Vote, Comment], safe=True)
  DATABASE.close()

