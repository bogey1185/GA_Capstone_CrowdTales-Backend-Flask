import os
from flask import Flask, g, flash, redirect, url_for
from resources.users import users_api
from resources.stories import stories_api
from resources.memberships import memberships_api                                                                                        
import config
import models
from flask_cors import CORS
from flask_login import LoginManager, current_user

app = Flask(__name__)

#session key for cookies 
app.secret_key = config.SECRET_KEY

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

CORS(users_api, origins=["http://localhost:3000"], supports_credentials=True)
CORS(stories_api, origins=["http://localhost:3000"], supports_credentials=True)
CORS(memberships_api, origins=["http://localhost:3000"], supports_credentials=True)
app.register_blueprint(users_api, url_prefix='/api/v1')
app.register_blueprint(stories_api, url_prefix='/api/v1')
app.register_blueprint(memberships_api, url_prefix='/api/v1')

@app.route('/')
def hello_world():
  return 'hello world'


if __name__ == '__main__':
  models.initialize()
  app.run(debug=config.DEBUG, port=config.PORT)


