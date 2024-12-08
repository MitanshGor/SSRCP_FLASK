from app import create_app
from flask_cors import CORS
from flask import Flask, request

app = create_app()
CORS(app) # resources= {
#     r"/*": {
#         "origins": "*",
#         "methods": ["GET", "POST", "DELETE", "OPTIONS"],
#         "allow_headers": ["Content-Type", "authorization","Accept"],
#     }})

# @app.before_request
# def handle_options(request):
#     if request.method == 'OPTIONS':
#         return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
