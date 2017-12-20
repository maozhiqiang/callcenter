from flask_cache import Cache
from flask_login import LoginManager

from flask_orm.webapp.models.user import User

# Setup flask cache
cache = Cache()

login_manager = LoginManager()


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)
