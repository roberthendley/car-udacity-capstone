from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug import Response
from .models import db, migrate
from .views import clients, contacts, reports
from auth import AuthError

# create and configure the app

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app, resources={r'/api/*': {"origins": "*"}})

    @app.after_request
    def after_request(response: Response):
        response.headers.add('Access-Control-Allow-Header',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
    API Routes - Health Check
    '''
    @app.route('/api/healthy',  methods=['GET'])
    def health_check():
        return jsonify({
            'success': True,
            'status': 'healthy'
        })

    '''
    Exception Handler - Bad Request (400)
    '''
    @app.errorhandler(400)
    @app.errorhandler(401)
    def bad_request(error):
        return return_error(400, 'The submitted request is invalid and ' +
                            'cannot be processed')

    '''
    Exception Handler - Unauthorised Request (403)
    '''
    @app.errorhandler(403)
    @app.errorhandler(AuthError)
    def unauthorised_request(error):
        return return_error(403, 'You are not authorised to perform the ' +
                            'request')

    '''
    Exception Handler - Resource Not Found (404)
    '''
    @app.errorhandler(404)
    def not_found(error):
        return return_error(404, 'The resource you requested could not ' +
                            'be found')

    '''
    Exception Handler - Method Not Allowed (405)
    '''
    @app.errorhandler(405)
    def not_allowed(error):
        return return_error(405, 'The action you have tried to perform on ' +
                            'the requested resource is not allowed')

    '''
    Exception Handler - Server Error (500)
    '''
    @app.errorhandler(500)
    def server_error(error):
        return_error(500, 'An error occurred on the server while trying ' +
            'to process your request')

    app.register_blueprint(clients.blueprint)
    app.register_blueprint(contacts.blueprint)
    app.register_blueprint(reports.blueprint)

    def return_error(error_code: int, message: str):
        return jsonify({
            'success': False,
            'message': message,
            'error_code': error_code
        }), error_code

    return app
