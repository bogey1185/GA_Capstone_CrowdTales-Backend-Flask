import os
from flask import Flask, g, flash, redirect, url_for
from resources.users import users_api
from resources.stories import stories_api
from resources.memberships import memberships_api   
from resources.storyqueues import storyqueues_api    
from resources.bookmarks import bookmarks_api      
from resources.contents import content_api   
from resources.comments import comment_api      
from resources.votes import votes_api                                                                         
import models
from flask_cors import CORS
from flask_login import LoginManager, current_user
# if not 'ON_HEROKU' in os.environ:
#   import config 

app = Flask(__name__)

#session key for cookies!
app.secret_key = 'LKSDFLKVNKNKSCNDMKLDMV SDLKMVNLKSD VSD'

#setup app login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
  try:
    return models.User.get(models.User.id == userid)
  except models.DoesNotExist:
    return None

CORS(users_api, origins=["http://localhost:3000", "https://crowdtales.herokuapp.com"], supports_credentials=True)
CORS(stories_api, origins=["http://localhost:3000", "https://crowdtales.herokuapp.com"], supports_credentials=True)
CORS(memberships_api, origins=["http://localhost:3000", "https://crowdtales.herokuapp.com"], supports_credentials=True)
CORS(storyqueues_api, origins=["http://localhost:3000", "https://crowdtales.herokuapp.com"], supports_credentials=True)
CORS(bookmarks_api, origins=["http://localhost:3000", "https://crowdtales.herokuapp.com"], supports_credentials=True)
CORS(content_api, origins=["http://localhost:3000", "https://crowdtales.herokuapp.com"], supports_credentials=True)
CORS(comment_api, origins=["http://localhost:3000", "https://crowdtales.herokuapp.com"], supports_credentials=True)
CORS(votes_api, origins=["http://localhost:3000", "https://crowdtales.herokuapp.com"], supports_credentials=True)
app.register_blueprint(users_api, url_prefix='/api/v1')
app.register_blueprint(stories_api, url_prefix='/api/v1')
app.register_blueprint(memberships_api, url_prefix='/api/v1')
app.register_blueprint(storyqueues_api, url_prefix='/api/v1')
app.register_blueprint(bookmarks_api, url_prefix='/api/v1')
app.register_blueprint(content_api, url_prefix='/api/v1')
app.register_blueprint(comment_api, url_prefix='/api/v1')
app.register_blueprint(votes_api, url_prefix='/api/v1')

@app.route('/')
def hello_world():
  return 'hello world'

if 'ON_HEROKU' in os.environ:
    models.initialize()
# else:
#   if __name__ == '__main__':
#     models.initialize()
#     app.run(debug=config.DEBUG, port=config.PORT)


