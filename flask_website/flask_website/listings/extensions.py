# -*- coding: utf-8 -*-
from urlparse import urlparse
from werkzeug import url_quote
from flask import Markup


class Extension(object):

    def __init__(self, name, author, description,
                 github=None, bitbucket=None, docs=None, website=None,
                 approved=False, notes=None):
        self.name = name
        self.author = author
        self.description = Markup(description)
        self.github = github
        self.bitbucket = bitbucket
        self.docs = docs
        self.website = website
        self.approved = approved
        self.notes = notes

    def to_json(self):
        rv = vars(self).copy()
        rv['description'] = unicode(rv['description'])
        return rv

    @property
    def pypi(self):
        return 'http://pypi.python.org/pypi/%s' % url_quote(self.name)

    @property
    def docserver(self):
        if self.docs:
            return urlparse(self.docs)[1]


# This list contains all extensions that were approved as well as those which
# passed listing.
extensions = [
    Extension('Flask-OAuth', 'Armin Ronacher',
        description='''
            <p>Adds <a href="http://oauth.net/">OAuth</a> support to Flask.
        ''',
        github='mitsuhiko/flask-oauth',
        docs='http://pythonhosted.org/Flask-OAuth/',
        notes='''
            Short long description, missing tests.
        '''
    ),
    Extension('Flask-OpenID', 'Armin Ronacher',
        description='''
            <p>Adds <a href="http://openid.net/">OpenID</a> support to Flask.
        ''',
        github='mitsuhiko/flask-openid',
        docs='http://pythonhosted.org/Flask-OpenID/',
        notes='''
            Short long description, missing tests.
        '''
    ),
    Extension('Flask-Babel', 'Armin Ronacher',
        description='''
            <p>Adds i18n/l10n support to Flask, based on
            <a href=http://babel.edgewall.org/>babel</a> and
            <a href=http://pytz.sourceforge.net/>pytz</a>.
        ''',
        github='mitsuhiko/flask-babel',
        docs='http://pythonhosted.org/Flask-Babel/',
        approved=True,
        notes='''
            How to improve: add a better long description to the next release.
        '''
    ),
    Extension('Flask-SQLAlchemy', 'Armin Ronacher',
        description='''
            <p>Add <a href="http://www.sqlalchemy.org/">SQLAlchemy</a> support to Flask
            with automatic configuration and helpers to simplify common web use cases.
            Major features include:</p>
            <ul>
            <li>Handle configuring one or more database connections.</li>
            <li>Set up sessions scoped to the request/response cycle.</li>
            <li>Time queries and track model changes for debugging.</li>
            </ul>
        ''',
        github='mitsuhiko/flask-sqlalchemy',
        docs='http://flask-sqlalchemy.pocoo.org/',
        approved=True
    ),
    Extension('Flask-Migrate', 'Miguel Grinberg',
        description='''
            <p><a href="http://www.sqlalchemy.org/">SQLAlchemy</a> database
            migrations for Flask applications using
            <a href="https://alembic.readthedocs.org/">Alembic</a>. The
            database operations are provided as command line arguments for
            <a href="https://flask-script.readthedocs.org/">Flask-Script</a>.
        ''',
        github='miguelgrinberg/flask-migrate',
        docs='http://pythonhosted.org/Flask-Migrate/',
    ),
    Extension('Flask-XML-RPC', 'Matthew Frazier',
        description='''
            <p>Adds <a href="http://www.xmlrpc.com/">XML-RPC</a> support to Flask.
        ''',
        bitbucket='leafstorm/flask-xml-rpc',
        docs='http://pythonhosted.org/Flask-XML-RPC/',
        approved=True
    ),
    Extension('Flask-CouchDB', 'Matthew Frazier',
        description='''
            <p>Adds <a href="http://couchdb.apache.org/">CouchDB</a> support to Flask.
        ''',
        bitbucket='leafstorm/flask-couchdb',
        docs='http://pythonhosted.org/Flask-CouchDB/',
        approved=True,
        notes='''
            There is also Flask-CouchDBKit.  Both are fine because they are
            doing different things, but the latter is not yet approved.
        '''
    ),
    Extension('Flask-Uploads', 'Max Countryman',
        description='''
            <p>Flask-Uploads allows your application to flexibly and
            efficiently handle file uploading and serving the uploaded files.
            You can create different sets of uploads - one for document
            attachments, one for photos, etc.
        ''',
        github='maxcountryman/flask-uploads',
        docs='https://flask-uploads.readthedocs.org/en/latest/',
        approved=True
    ),
    Extension('Flask-Themes', 'Matthew Frazier',
        description='''
            <p>Flask-Themes makes it easy for your application to support
            a wide range of appearances.
        ''',
        bitbucket='leafstorm/flask-themes',
        docs='http://pythonhosted.org/Flask-Themes/',
        approved=True
    ),
    Extension('Flask-CouchDBKit', 'Kridsada Thanabulpong',
        description='''
            <p>Adds <a href="http://www.couchdbkit.org/">CouchDBKit</a> support to Flask.
        ''',
        github='sirn/flask-couchdbkit',
        docs='http://pythonhosted.org/Flask-CouchDBKit/'
    ),
    Extension('Flask-Genshi', 'Dag Odenhall',
        description='''
            <p>Adds support for the <a href="http://genshi.edgewall.org/">Genshi</a>
            templating language to Flask applications.
        ''',
        github='dag/flask-genshi',
        docs='http://pythonhosted.org/Flask-Genshi/',
        approved=True,
        notes='''
            This is the first template engine extension.  When others come
            around it would be a good idea to decide on a common interface.
        '''
    ),
    Extension('Flask-Mail', 'Matt Wright (created by Dan Jacob)',
        description='''
            <p>Makes sending mails from Flask applications very easy and
            has also support for unittesting.
        ''',
        github='mattupstate/flask-mail',
        docs='http://pythonhosted.org/Flask-Mail/',
        approved=True
    ),
    Extension('Flask-WTF', 'Anthony Ford (created by Dan Jacob)',
        description='''
            <p>Flask-WTF offers simple integration with WTForms. This
            integration includes optional CSRF handling for greater security.
        ''',
        github='ajford/flask-wtf',
        docs='http://pythonhosted.org/Flask-WTF/',
        approved=True
    ),
    Extension('Flask-Testing', u'Christoph Heer (created by Dan Jacob)',
        description='''
            <p>The Flask-Testing extension provides unit testing utilities for Flask.
        ''',
        github='jarus/flask-testing',
        docs='http://pythonhosted.org/Flask-Testing/',
        approved=True
    ),
    Extension('Flask-Script', 'Sean Lynch (created by Dan Jacob)',
        description='''
            <p>The Flask-Script extension provides support for writing external
            scripts in Flask. It uses argparse to parse command line arguments.
        ''',
        github='techniq/flask-script',
        docs='http://pythonhosted.org/Flask-Script/',
        approved=True,
        notes='''
            Flask-Actions has some overlap.  Consider that when approving
            Flask-Actions or similar packages.
        '''
    ),
    Extension('flask-lesscss', 'Steve Losh',
        description='''
            <p>
              A small Flask extension that makes it easy to use
              <a href=http://lesscss.org/>LessCSS</a> with your
              Flask application.
        ''',
        docs='http://sjl.bitbucket.org/flask-lesscss/',
        bitbucket='sjl/flask-lesscss',
        notes='''
            Broken package description, nonconforming package name, does not
            follow standard API rules (init_lesscss instead of lesscss).

            Considered for unlisting, improved version should release as
            "Flask-LessCSS" with a conforming API and fixed packages indices,
            as well as a testsuite.
        '''
    ),
    Extension('Flask-Creole', 'Ali Afshar',
        description='''
            <p>Creole parser filters for Flask.
        ''',
        docs='http://pythonhosted.org/Flask-Creole',
        bitbucket='aafshar/flask-creole-main',
        approved=True,
        notes='''
            Flask-Markdown and this should share API, consider that when
            approving Flask-Markdown
        '''
    ),
    Extension('Flask-Cache', 'Thadeus Burgess',
        description='''
            <p>Adds cache support to your Flask application.
        ''',
        docs='http://pythonhosted.org/Flask-Cache',
        github='thadeusb/flask-cache',
    ),
    Extension('Flask-Principal', 'Ali Afshar',
        description='''
            <p>Identity management for Flask.
        ''',
        docs='http://pythonhosted.org/Flask-Principal',
        github='mattupstate/flask-principal',
        approved=False
    ),
    Extension('Flask-Zen', 'Noah Kantrowitz',
        description='''
            <p>Flask-Zen allows you to use PyZen via Flask-Script commands.
        ''',
        docs='http://pythonhosted.org/Flask-Zen/',
        github='coderanger/flask-zen',
        approved=False
    ),
    Extension('Flask-Static-Compress', 'Alan Hamlett',
        description='''
            <p>Automatically minifies, combines, and versions your static CSS
              and JavaScript assets. Like Django-Compressor for Flask.
        ''',
        github='alanhamlett/flask-static-compress',
        docs='https://github.com/alanhamlett/flask-static-compress',
        approved=False
    ),
    Extension('Flask-Assets', u'Michael Elsdörfer',
        description='''
            <p>
              Integrates the webassets library with Flask, adding support for
              merging, minifying and compiling CSS and Javascript files.
        ''',
        docs='http://elsdoerfer.name/docs/flask-assets/',
        github='miracle2k/flask-assets',
        approved=False
    ),
    Extension('Flask-AutoIndex', 'Heungsub Lee',
        description='''
            <p>
              An extension that generates an index page for your Flask
              application automatically
        ''',
        docs='http://pythonhosted.org/Flask-AutoIndex/',
        github='sublee/flask-autoindex',
        approved=False
    ),
    Extension('Flask-Celery', 'Ask Solem',
        description='''
            <p>
              Celery integration for Flask
        ''',
        docs='http://ask.github.com/celery/',
        github='ask/flask-celery',
        approved=False
    ),
    Extension('Flask-Cors', 'Cory Dolphin',
        description='''
            <p>
              Cross Origin Resource Sharing (CORS)  for flask
        ''',
        docs='http://flask-cors.readthedocs.org/en/latest/',
        github='wcdolphin/flask-cors',
        approved=False
    ),
    Extension('Frozen-Flask', 'Simon Sapin',
        description='''
            <p>
              Freezes a Flask application into a set of static files.
              The result can be hosted without any server-side software
              other than a traditional web server.
        ''',
        docs='http://pythonhosted.org/Frozen-Flask/',
        github='SimonSapin/Frozen-Flask',
        approved=True
    ),
    Extension('Flask-FlatPages', 'Simon Sapin',
        description='''
            <p>
              Provides flat static pages to a Flask application, based on text
              files as opposed to a relational database.
        ''',
        docs='http://pythonhosted.org/Flask-FlatPages/',
        github='SimonSapin/Flask-FlatPages',
        approved=True
    ),
    Extension('Flask-FluidDB', 'Ali Afshar',
        description='''
            <p>
              FluidDB access for Flask.
        ''',
        docs='http://pythonhosted.org/Flask-FluidDB/',
        bitbucket='aafshar/flask-fluiddb-main',
        approved=False
    ),
    Extension('Flask-fillin', 'Christoph Heer',
        description='''
            <p>The Flask-fillin extension provides simple utilities for testing your forms in Flask application..
        ''',
        github='jarus/flask-fillin',
        docs='http://pythonhosted.org/Flask-fillin/',
    ),
    Extension('Flask-Gravatar', 'Zelenyak Aleksandr',
        description='''
            <p>
              Small extension for Flask to make using Gravatar easy.
        ''',
        docs='http://pythonhosted.org/Flask-Gravatar/',
        github='zzzsochi/Flask-Gravatar',
        approved=False
    ),
    Extension('Flask-HTMLBuilder', 'Zahari Petkov',
        description='''
            <p>
              Flask-HTMLBuilder is an extension that allows flexible and easy
              Python-only generation of HTML snippets and full HTML documents
              using a robust syntax.
        ''',
        docs='http://majorz.github.com/flask-htmlbuilder/',
        github='majorz/flask-htmlbuilder',
        approved=False
    ),
    Extension('Flask-MongoAlchemy', 'Francisco Souza',
        description='''
            <p>
              Add Flask support for MongoDB using MongoAlchemy.
        ''',
        docs='http://pythonhosted.org/Flask-MongoAlchemy/',
        github='cobrateam/flask-mongoalchemy',
        approved=False
    ),
    Extension('Flask-DebugToolbar', 'Matt Good',
        description='''
            <p>
              A port of the Django debug toolbar to Flask
        ''',
        docs='https://github.com/mgood/flask-debugtoolbar',
        github='mgood/flask-debugtoolbar',
        approved=False
    ),
    Extension('Flask-Login', 'Matthew Frazier',
        description='''
            <p>
              Flask-Login provides user session management for Flask. It
              handles the common tasks of logging in, logging out, and
              remembering your users' sessions over extended periods of time.
        ''',
        github='maxcountryman/flask-login',
        docs='http://pythonhosted.org/Flask-Login/',
        approved=True
    ),
    Extension('Flask-Security', 'Matt Wright',
        description='''
            <p>
              Flask-Security is an opinionated Flask extension which adds
              basic security and authentication features to your Flask apps
              quickly and easily.
        ''',
        docs='https://pythonhosted.org/Flask-Security/',
        github='mattupstate/flask-security'
    ),
    Extension('Flask-Exceptional', 'Jonathan Zempel',
        description='''
            <p>
              Adds Exceptional support to Flask applications
        ''',
        docs='http://pythonhosted.org/Flask-Exceptional/',
        github='jzempel/flask-exceptional',
        approved=True,
    ),
    Extension('Flask-Bcrypt', 'Max Countryman',
        description='''
            <p>
              Bcrypt support for hashing passwords
        ''',
        docs='http://pythonhosted.org/Flask-Bcrypt/',
        github='maxcountryman/flask-bcrypt',
        approved=True,
    ),
    Extension('Flask-MongoKit', 'Christoph Heer',
        description='''
            <p>
              Flask extension to better integrate MongoKit into Flask
        ''',
        docs='http://pythonhosted.org/Flask-MongoKit/',
        github='jarus/flask-mongokit'
    ),
    Extension('Flask-GAE-Mini-Profiler', 'Pascal Hartig',
        description='''
            <p>
              Flask integration of gae_mini_profiler for Google App Engine.
        ''',
        docs='http://pythonhosted.org/Flask-GAE-Mini-Profiler',
        github='passy/flask-gae-mini-profiler'
    ),
    Extension('Flask-Admin', 'Flask-Admin team',
        description='''
            <p>Simple and extensible administrative interface framework for Flask
        ''',
        docs='http://flask-admin.readthedocs.org/en/latest/index.html',
        github='flask-admin/flask-admin'
    ),
    Extension('Flask-ZODB', 'Dag Odenhall',
        description='''
            <p>
              Use the ZODB with Flask
        ''',
        docs='http://pythonhosted.org/Flask-ZODB/',
        github='dag/flask-zodb',
        approved=True
    ),
    Extension('Flask-Peewee', 'Charles Leifer',
        description='''
            <p>
              Integrates Flask and the peewee orm
        ''',
        docs='http://charlesleifer.com/docs/flask-peewee/index.html',
        github='coleifer/flask-peewee',
        approved=False
    ),
    Extension('Flask-Lettuce', 'Daniel, Dao Quang Minh',
        description='''
            <p>
              Add Lettuce support for Flask
        ''',
        # docs='http://pythonhosted.org/Flask-Lettuce/',
        github='dqminh/flask-lettuce',
        approved=False
    ),
    Extension('Flask-Sijax', 'Slavi Pantaleev',
        description='''
            <p>
              Flask integration for Sijax,
              a Python/jQuery library that makes AJAX easy to use
        ''',
        docs='http://pythonhosted.org/Flask-Sijax/',
        github='spantaleev/flask-sijax',
        approved=False
    ),
    Extension('Flask-Dashed', 'Jean-Philippe Serafin',
        description='''
            <p>
              Flask-Dashed provides tools for building
              simple and extensible admin interfaces.
        ''',
        docs='http://jeanphix.github.com/Flask-Dashed/',
        github='jeanphix/Flask-Dashed',
        approved=False
    ),
    Extension('Flask-SeaSurf', 'Max Countryman',
        description='''
            <p>
              SeaSurf is a Flask extension for preventing
              cross-site request forgery (CSRF).
        ''',
        docs='http://pythonhosted.org/Flask-SeaSurf/',
        github='maxcountryman/flask-seasurf',
        approved=True,
    ),
    Extension('Flask-PonyWhoosh', 'Jonathan Prieto-Cubides & Felipe Rodriguez',
        description='''
            <p>
              A full-text search engine using Pony ORM and Whoosh.
        ''',
        docs='http://pythonhosted.org/flask-ponywhoosh/',
        github='compiteing/flask-ponywhoosh',
    ),
    Extension('Flask-PyMongo', 'Dan Crosta',
        description='''
            <p>
              Flask-PyMongo bridges Flask and PyMongo.
        ''',
        docs='http://readthedocs.org/docs/flask-pymongo/',
        github='dcrosta/flask-pymongo',
    ),
    Extension('Flask-Raptor', 'Dan Lepage',
        description='''
            <p>
              Flask-Raptor provides support for adding raptors
              to Flask instances.
        ''',
        docs='http://pythonhosted.org/Flask-Raptor/',
        github='dplepage/flask-raptor',
    ),
    Extension('Flask-Shelve', 'James Saryerwinnie',
        description='''
            <p>
              Flask-Shelve bridges Flask and the Python standard library
              `shelve` module, for very simple (slow) no-dependency key-value
              storage.
        ''',
        docs='http://pythonhosted.org/Flask-Shelve/',
        github='jamesls/flask-shelve',
    ),
    Extension('Flask-RESTful', 'Twilio API Team',
        description='''
            <p>Flask-RESTful provides the building blocks for creating a great REST API.
        ''',
        docs='https://flask-restful.readthedocs.org/',
        github='flask-restful/flask-restful',
        approved=True
    ),
    Extension('Flask-Restless', 'Jeffrey Finkelstein',
        description='''
            <p>Flask-Restless provides simple generation of ReSTful APIs for
              database models defined using Flask-SQLAlchemy. The generated
              APIs send and receive messages in JSON format.
        ''',
        docs='http://readthedocs.org/docs/flask-restless/en/latest/',
        github='jfinkels/flask-restless',
        approved=True
    ),
    Extension('Flask-Heroku', 'Kenneth Reitz',
        description='''
            <p>Sets Flask configuration defaults for Heroku-esque environment variables
        ''',
        github='kennethreitz/flask-heroku',
        approved=False
    ),
    Extension('Flask-Mako', 'Beranger Enselme, Frank Murphy',
        description='''
            <p>Allows for <a href="http://www.makotemplates.org/">Mako templates</a>
            to be used instead of Jinja2
        ''',
        github='benselme/flask-mako',
        docs='http://pythonhosted.org/Flask-Mako/',
        approved=False
    ),
    Extension('Flask-WeasyPrint', 'Simon Sapin',
        description='''
            <p>Make PDF with <a href="http://weasyprint.org/">WeasyPrint</a>
               in your Flask app.
        ''',
        docs='http://pythonhosted.org/Flask-WeasyPrint/',
        github='SimonSapin/Flask-WeasyPrint',
    ),
    Extension('Flask-Classy', 'Freedom Dumlao',
        description='''
            <p>Class based views for Flask.
        ''',
        github='apiguy/flask-classy',
        docs='http://pythonhosted.org/Flask-Classy/',
        approved=False
    ),
    Extension('Flask-WebTest', 'Anton Romanovich',
        description='''
            <p>Utilities for testing Flask applications with
               <a href="http://webtest.readthedocs.org/en/latest/">WebTest</a>.
        ''',
        github='aromanovich/flask-webtest',
        docs='http://flask-webtest.readthedocs.org/',
        approved=False
    ),
    Extension('Flask-Misaka', 'David Baumgold',
        description='''
            A simple extension to integrate the
            <a href="http://misaka.61924.nl/">Misaka</a> module for efficiently
            parsing Markdown.
        ''',
        docs='https://flask-misaka.readthedocs.org/en/latest/',
        github='singingwolfboy/flask-misaka',
        approved=True,
    ),
    Extension('Flask-Dance', 'David Baumgold',
        description='''
            Doing the OAuth dance with style using Flask, requests, and oauthlib.
        ''',
        docs='https://flask-dance.readthedocs.org/en/latest/',
        github='singingwolfboy/flask-dance',
        approved=True,
    ),
    Extension('Flask-SSE', 'David Baumgold',
        description='''
            <a href="http://www.html5rocks.com/en/tutorials/eventsource/basics/">
            Server Sent Events</a> for Flask.
        ''',
        docs='https://flask-sse.readthedocs.org/en/latest/',
        github='singingwolfboy/flask-sse',
        approved=True,
    ),
    Extension('Flask-Limiter', 'Ali-Akber Saifee',
              description='''
            <p>Adds Ratelimiting support to Flask.
            Supports a configurable storage backend with implementations for
            in-memory, redis and memcache.
        ''',
        github='alisaifee/flask-limiter',
        docs='http://flask-limiter.readthedocs.org/en/latest/',
        approved=False,
    ),
    Extension('Flask-User', 'Ling Thio',
        description='''
            Customizable User Account Management for Flask:
            Register, Confirm email, Login, Change username, Change password, Forgot password,
            Role-based Authorization and Internationalization.
        ''',
        github='lingthio/flask-user',
        docs='http://pythonhosted.org/Flask-User/',
        approved=True,
    ),
    Extension('Flask-Via', 'SOON_, Chris Reeves',
        description='''
            <p>
                Provides a clean, simple URL routing framework for growing Flask
                Applications.
        ''',
        docs='http://flask-via.soon.build',
        github='thisissoon/Flask-Via',
    ),
    Extension('Flask-QueryInspect', 'Bret Barker',
        description='''
            <p>Provides metrics on SQL queries (using SQLAlchemy) executed
             for each request.</p>
        ''',
        docs='https://github.com/noise/flask-queryinspect',
        github='noise/flask-queryinspect',
    ),
    Extension('Flask-Stormpath', 'Randall Degges',
        description='''
            <p>Add Stormpath user management, authentication,
            and authorization to Flask.
        ''',
        docs='http://flask-stormpath.readthedocs.org/en/latest/',
        github='stormpath/stormpath-flask'
    ),
    Extension('Flask-Ask', 'John Wheeler',
        description='''
            <p>
              Flask-Ask makes it easy to write Amazon Echo apps with Flask and
              the Alexa Skills Kit.
        ''',
        docs='http://flask-ask.readthedocs.io/en/latest/',
        github='johnwheeler/flask-ask'
    ),
    Extension('Flask-Rest-JSONAPI', 'Pierre Chaisy',
        description='''
            <p>
              Build REST APIs following the
              <a href="http://jsonapi.org/format/">JSONAPI</a>
              specification with a powerful data layer system.
        ''',
        docs='http://flask-rest-jsonapi.readthedocs.io/en/latest/',
        github='miLibris/flask-rest-jsonapi'
    ),
]


# This is a list of extensions that is currently rejected from listing and with
# that also not approved.  If an extension ends up here it should improved to
# be listed.
unlisted = [
    Extension('Flask-Actions', 'Young King',
        description='''
            <p>
              Flask-actions provide some management comands for flask based
              project.
        ''',
        docs='http://pythonhosted.org/Flask-Actions/',
        bitbucket='youngking/flask-actions',
        approved=False,
        notes='''
            Rejected because of missing description in PyPI, formatting issues
            with the documentation (missing headlines, scrollbars etc.) and a
            general clash of functionality with the Flask-Script package.
            Latter should not be a problem, but the documentation should
            improve.  For listing, the extension developer should probably
            discuss the extension on the mailinglist with others.

            Futhermore it also has an egg registered with an invalid filename.
        '''
    ),
    Extension('Flask-Jinja2Extender', 'Dan Colish',
        description='''
            <p>
        ''',
        docs=None,
        github='dcolish/flask-jinja2extender',
        approved=False,
        notes='''
            Appears to be discontinued.

            Usecase not obvious, hacky implementation, does not solve a problem
            that could not be solved with Flask itself.  I suppose it is to aid
            other extensions, but that should be discussed on the mailinglist.
        '''
    ),
    Extension('Flask-Markdown', 'Dan Colish',
        description='''
            <p>
              This is a small module to a markdown processing filter into your
              flask.
        ''',
        docs='http://pythonhosted.org/Flask-Markdown/',
        github='dcolish/flask-markdown',
        approved=False,
        notes='''
            Would be great for enlisting but it should follow the API of
            Flask-Creole.  Besides that, the docstrings are not valid rst (run
            through rst2html to see the issue) and it is missing tests.
            Otherwise fine :)
        '''
    ),
    Extension('flask-urls', 'Steve Losh',
        description='''
            <p>
              A collection of URL-related functions for Flask applications.
        ''',
        docs='http://sjl.bitbucket.org/flask-urls/',
        bitbucket='sjl/flask-urls',
        approved=False,
        notes='''
            Broken PyPI index and non-conforming extension name.  Due to the
            small featureset this was also delisted from the list.  It was
            there previously before the approval process was introduced.
        '''
    ),
    Extension('Flask-Coffee', 'Col Wilson',
        description='''
            <p>
              Automatically compile CoffeeScript files while developing with
              the Flask framework.
        ''',
        docs=None,
        approved=False,
        notes='''
            On the mailing list, author claims it's flask-lesscss with a
            different label.  No sphinx-based docs, just a blog post.  No
            publicly accessible repository -- requires login on
            bettercodes.org.
        '''
    ),
    Extension('Flask-Solr', 'Ron DuPlain',
        description='''
            <p>
              Add Solr support to Flask using pysolr.
        ''',
        docs=None,
        github='willowtreeapps/flask-solr',
        notes='''
            Fully exposes pysolr API in Flask extension pattern, and code is
            production-ready.  It lacks documentation and tests.
        '''
    ),
    Extension('flask-csrf', 'Steve Losh',
        description='''
            <p>A small Flask extension for adding
            <a href=http://en.wikipedia.org/wiki/CSRF>CSRF</a> protection.
        ''',
        docs='http://sjl.bitbucket.org/flask-csrf/',
        bitbucket='sjl/flask-csrf',
        notes='''
            Unlisted because duplicates the Flask-SeaSurf extension.
        '''
    ),
]


extensions.sort(key=lambda x: x.name.lower())
unlisted.sort(key=lambda x: x.name.lower())
