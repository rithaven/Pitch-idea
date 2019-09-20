from app import creat_app,db
from flask_script import Manager,Server
from app.models import User
from flask_migrate import Migrate,MigrateCommand
