from flask import Blueprint, abort, jsonify, request
from sqlalchemy import select

from auth import requires_auth
from models import Movie

bp = Blueprint('movie', __name__)


@bp.route('/', methods=['GET'])
@requires_auth('get:movies')
def get_movies(jwt):
    movies = Movie.query.all()
    return jsonify({'movies': [movie.format() for movie in movies]})


@bp.route('/', methods=['POST'])
@requires_auth('post:movies')
def create_movie(jwt):
    body = request.get_json()

    if 'title' not in body:
        abort(422)

    if Movie.query.filter(Movie.title == body.get('title')).first():
        abort(409)

    try:
        movie = Movie(title=body.get('title'),
                      releaseDate=body.get('releaseDate', None)
                      )
        movie.insert()
        return jsonify({'movie': movie.format()})

    except Exception:
        abort(422)


@bp.route('/<int:id>', methods=['GET'])
@requires_auth('get:movies')
def get_movie(jwt, id):
    movie = Movie.query.get_or_404(id)
    return jsonify({'movie': movie.format()})


@bp.route('/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(jwt, id):
    body = request.get_json()
    movie = Movie.query.get_or_404(id)

    if 'title' in body and body.get('title') != movie.title:
        if Movie.query.filter(Movie.title == body.get('title')).first():
            abort(409)
        movie.title = body.get('title')

    if 'releaseDate' in body and body.get('releaseDate') != movie.releaseDate:
        movie.releaseDate = body.get('releaseDate')

    try:
        movie.update()
        return jsonify({'movie': movie.format()})

    except Exception:
        abort(422)


@bp.route('/<int:id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(jwt, id):
    movie = Movie.query.get_or_404(id)

    try:
        movie.delete()
        return jsonify(), 204

    except Exception:
        abort(422)
