from flask_restful import Api, Resource
from flask import Blueprint

# Create Blueprint for API routes
api_prefix = Blueprint('api_prefix', __name__)
api = Api(api_prefix)

# Base route handler
class BaseAPI(Resource):
    def get(self):
        return "up"

# Add base route to indicate API status
api.add_resource(BaseAPI, "/")

# Import route handlers
from .AnonymizeCSVHandler import AnonymizeCSVHandler
from .AnonymizeTextHandler import AnonymizeTextHandler

# Add route handlers to API
api.add_resource(AnonymizeCSVHandler, '/anonymize/csv/')
api.add_resource(AnonymizeTextHandler, '/anonymize/text/')