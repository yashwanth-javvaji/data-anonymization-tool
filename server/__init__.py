from flask_cors import CORS
from flask import Flask
from .routes import api_prefix

def create_app():
    # Create Flask application instance
    app = Flask(__name__)
    
    # Enable CORS for all routes and origins
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register Blueprint for API routes with prefix
    app.register_blueprint(api_prefix, url_prefix = '/api')

    # Return Flask application instance
    return app