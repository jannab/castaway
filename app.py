from flask import Flask, jsonify

import os

from routes import actor, errors, movie
from models import db

DB_PATH = os.getenv('DB_PATH', 'postgresql://postgres@127.0.0.1:5432/castaway')


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(SQLALCHEMY_DATABASE_URI=DB_PATH)

    if test_config is not None:
        app.config.from_mapping(test_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(errors.bp)
    app.register_blueprint(actor.bp, url_prefix='/actors')
    app.register_blueprint(movie.bp, url_prefix='/movies')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=8080, debug=True)
