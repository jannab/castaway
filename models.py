import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


movie_casts = db.Table('movie_casts',
                       db.Column('movie_id', db.Integer,
                                 db.ForeignKey('movies.id'),
                                 primary_key=True),
                       db.Column('actor_id', db.Integer,
                                 db.ForeignKey('actors.id'),
                                 primary_key=True)
                       )


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': [movie.title for movie in self.movies]
            }

    def __repr__(self):
        return f'<Actor {self.name} (id: {self.id})>'


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    releaseDate = Column(String)
    actors = db.relationship('Actor', secondary=movie_casts,
                             backref=db.backref('movies', lazy=True))

    def __init__(self, title, releaseDate):
        self.title = title
        self.releaseDate = releaseDate

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'releaseDate': self.releaseDate,
            'actors': [actor.name for actor in self.actors]
            }

    def __repr__(self):
        return f'<Movie {self.title} (id: {self.id})>'
