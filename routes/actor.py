from flask import Blueprint, abort, jsonify, request

from auth import requires_auth
from models import Actor

bp = Blueprint('actor', __name__)


@bp.route('/', methods=['GET'])
@requires_auth('get:actors')
def get_actors(jwt):
    actors = Actor.query.all()
    return jsonify({'actors': [actor.format() for actor in actors]})


@bp.route('/', methods=['POST'])
@requires_auth('post:actors')
def create_actor(jwt):
    body = request.get_json()

    if 'name' not in body:
        abort(422)

    if Actor.query.filter(Actor.name == body.get('name')).first():
        abort(409)

    try:
        actor = Actor(name=body.get('name'),
                      age=body.get('age', None),
                      gender=body.get('gender', None)
                      )
        actor.insert()
        return jsonify({'actor': actor.format()})

    except Exception:
        abort(422)


@bp.route('/<int:id>', methods=['GET'])
@requires_auth('get:actors')
def get_actor(jwt, id):
    actor = Actor.query.get_or_404(id)
    return jsonify({'actor': actor.format()})


@bp.route('/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(jwt, id):
    body = request.get_json()
    actor = Actor.query.get_or_404(id)

    if 'name' in body and body.get('name') != actor.name:
        if Actor.query.filter(Actor.name == body.get('name')).first():
            abort(409)
        actor.name = body.get('name')

    if 'age' in body and body.get('age') != actor.age:
        actor.age = body.get('age')

    if 'gender' in body and body.get('gender') != actor.gender:
        actor.gender = body.get('gender')

    try:
        actor.update()
        return jsonify({'actor': actor.format()})

    except Exception:
        abort(422)


@bp.route('/<int:id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(jwt, id):
    actor = Actor.query.get_or_404(id)

    try:
        actor.delete()
        return jsonify(), 204

    except Exception:
        abort(422)
