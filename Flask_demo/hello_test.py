# -*- encoding: utf-8 -*-

from flask import Flask
app = Flask(__name__)
app.config.from_object('config')
#app.config.from_object('yourapplication.default_settings')


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/index/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

#app.

if __name__ == '__main__':
    app.run()