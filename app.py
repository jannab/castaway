from flask import Flask, jsonify

from routes import actor, errors, movie
from models import setup_db


def create_app(test_config=None):
    app = Flask(__name__)
    app.app_context().push()
    setup_db(app)
    app.register_blueprint(errors.bp)
    app.register_blueprint(actor.bp, url_prefix='/actors')
    app.register_blueprint(movie.bp, url_prefix='/movies')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=8080, debug=True)
