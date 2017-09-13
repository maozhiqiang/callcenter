from datetime import datetime
from flask import Flask, session, g, render_template
from flask_openid import OpenID

app = Flask(__name__)
app.config.from_object('websiteconfig')

from openid_auth import DatabaseOpenIDStore
oid = OpenID(app, store_factory=DatabaseOpenIDStore)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.before_request
def load_current_user():
    g.user = User.query.filter_by(openid=session['openid']).first() \
        if 'openid' in session else None


@app.teardown_request
def remove_db_session(exception):
    db_session.remove()


@app.context_processor
def current_year():
    return {'current_year': datetime.utcnow().year}


app.add_url_rule('/docs/', endpoint='docs.index', build_only=True)
app.add_url_rule('/docs/<path:page>/', endpoint='docs.show',
                 build_only=True)
app.add_url_rule('/docs/<version>/.latex/Flask.pdf', endpoint='docs.pdf',
                 build_only=True)

from views import general
from views import community
from views import mailinglist
from views import snippets
from views import extensions
app.register_blueprint(general.mod)
app.register_blueprint(community.mod)
app.register_blueprint(mailinglist.mod)
app.register_blueprint(snippets.mod)
app.register_blueprint(extensions.mod)

from database import User, db_session
import utils

app.jinja_env.filters['datetimeformat'] = utils.format_datetime
app.jinja_env.filters['dateformat'] = utils.format_date
app.jinja_env.filters['timedeltaformat'] = utils.format_timedelta
app.jinja_env.filters['displayopenid'] = utils.display_openid
