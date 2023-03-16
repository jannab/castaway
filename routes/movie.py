from flask import Blueprint, abort, jsonify, request
from sqlalchemy import select

from models import Movie

bp = Blueprint('movie', __name__)

@bp.route('/', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify([movie.format() for movie in movies])

@bp.route('/', methods=['POST'])
def create_movie():
    body = request.get_json()

    if not 'title' in body:
        abort(422)

    if Movie.query.filter(Movie.title == body.get('title')).first():
        abort(409)

    try:
        movie = Movie(title=body.get('title'),
                      releaseDate=body.get('releaseDate', None)
                      )
        movie.insert()
        return jsonify(movie.format())

    except Exception:
        abort(422)

@bp.route('/<int:id>', methods=['GET'])
def get_movie(id):
    movie = Movie.query.get_or_404(id)
    return jsonify(movie.format())

@bp.route('/<int:id>', methods=['PATCH'])
def update_movie(id):
    body = request.get_json()
    movie = Movie.query.get_or_404(id)

    if 'title' in body:
        if Movie.query.filter(Movie.title == body.get('title')).first():
            abort(409)
        movie.title = body.get('title')

    if 'releaseDate' in body:
        movie.releaseDate = body.get('releaseDate')

    try:
        movie.update()
        return jsonify(movie.format())

    except Exception:
        abort(422)

@bp.route('/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.query.get_or_404(id)

    try:
        movie.delete()
        return jsonify(), 204

    except Exception:
        abort(422)
