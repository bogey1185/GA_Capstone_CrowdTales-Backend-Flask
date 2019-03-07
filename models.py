class User(UserMixin, Model):
  username      = CharField(unique=True)
  email         = CharField(unique=True)
  password      = CharField()
  stories       = ForeignKeyField(Story, backref='stories')
  memberships   = ForeignKeyField(Membership, backref='membership')
  bookmarks     = ForeignKeyField(Bookmarks, backref='bookmarks')


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
 
class Content(Model):
  username  = ForeignKeyField(User, backref='user') 
  date      = DateTimeField(default=datetime.datetime.now)
  text      = TextField()
  votes     = ForeignKeyField(Vote, backref='vote')
  comments  = ForeignKeyField(Comment, backref='comment')
  votedate  = DateTimeField() 

class Membership(Model): # this model tracks stories where user has contributed
  username  = ForeignKeyField(User, backref='user')
  story     = ForeignKeyField(Story, backref='story')

class StoryQueue(Model): # this model tracks stories where user is queued to contribute
  username  = ForeignKeyField(User, backref='user')
  story     = ForeignKeyField(Story, backref='story')

class Bookmark(Model): #this model used to track stories that user wants to follow, but not contribute
  username  = ForeignKeyField(User, backref='user')
  story     = ForeignKeyField(Story, backref='story')

class Vote(Model):
  username  = ForeignKeyField(User, backref='user')
  vote      = CharField()
  content   = ForeignKeyField(Content, backref='content')

class Comment(Model): 
  username  = ForeignKeyField(User, backref='user')
  date      = DateTimeField(default=datetime.datetime.now)
  text      = TextField()
  comments  = ForeignKeyField('self')




