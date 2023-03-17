from flask import Blueprint, abort, jsonify, request

from models import Actor

bp = Blueprint('actor', __name__)

@bp.route('/', methods=['GET'])
def get_actors():
    actors = Actor.query.all()
    return jsonify({'actors': [actor.format() for actor in actors]})

@bp.route('/', methods=['POST'])
def create_actor():
    body = request.get_json()

    if not 'name' in body:
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
def get_actor(id):
    actor = Actor.query.get_or_404(id)
    return jsonify({'actor': actor.format()})

@bp.route('/<int:id>', methods=['PATCH'])
def update_actor(id):
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
def delete_actor(id):
    actor = Actor.query.get_or_404(id)

    try:
        actor.delete()
        return jsonify(), 204

    except Exception:
        abort(422)
