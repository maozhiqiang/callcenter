from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

class UserAPI(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


api.add_resource(UserAPI, '/users/<int:id>', endpoint = 'user')
if __name__ == '__main__':
    app.run()