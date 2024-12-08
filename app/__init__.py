from flask import Flask
from .routes.carControl import control_routes
from flask_cors import CORS


# from .routes.vehicleSet import vehicle_routes
def create_app():
    
    app = Flask(__name__)    
    # CORS(app, resources= {
    # r"/*": {
    #     "origins": "*",
    #     "methods": ["GET", "POST", "DELETE", "OPTIONS"],
    #      "allow_headers": ["Content-Type", "authorization","Accept"],
    # }});

    # Register Blueprints
    # app.register_blueprint(vehicle_routes, url_prefix='/vehicle')
    app.register_blueprint(control_routes, url_prefix='/control')


    return app
