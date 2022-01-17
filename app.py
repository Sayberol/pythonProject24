# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    genre = fields.Str()
    director_id = fields.Int()
    director = fields.Str()


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


movie_schema = MovieSchema()
genre_schema = GenreSchema()
director_schema = DirectorSchema()


api = Api(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        result = Movie.query
        if director_id is not None:
            result = result.filter(Movie.director_id == director_id)
        if genre_id is not None:
            result = result.filter(Movie.genre_id == genre_id)
        total_result = result.all()

        return movie_schema.dump(total_result, many=True)

    def post(self):
        req_json = request.json
        add_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(add_movie)
        return "", 201


@movie_ns.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid):
        movie = Movie.query.get(uid)
        if not movie:
            return "", 404
        return movie_schema.dump(movie)

    def delete(self, uid):
        movie = Movie.query.get(uid)
        if not movie:
            return "", 404
        else:
            db.session.delete(movie)
            db.session.commit()
            return "", 204


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        result = Director.query
        total_result = result.all()

        return director_schema.dump(total_result, many=True)

    def post(self):
        req_json = request.json
        add_director = Director(**req_json)
        with db.session.begin():
            db.session.add(add_director)
        return "", 201


@director_ns.route('/<int:uid>')
class DirectorView(Resource):
    def get(self, uid):
        director = Director.query.get(uid)
        if not director:
            return "", 404
        return director_schema.dump(director)

    def delete(self, uid):
        director = Director.query.get(uid)
        if not director:
            return "", 404
        else:
            db.session.delete(director)
            db.session.commit()
            return "", 204


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        result = Genre.query
        total_result = result.all()

        return genre_schema.dump(total_result, many=True)

    def post(self):
        req_json = request.json
        add_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(add_genre)
        return "", 201


@genre_ns.route('/<int:uid>')
class GenreView(Resource):
    def get(self, uid):
        genre = Genre.query.get(uid)
        if not genre:
            return "", 404
        return genre_schema.dump(genre)

    def delete(self, uid):
        genre = Genre.query.get(uid)
        if not genre:
            return "", 404
        else:
            db.session.delete(genre)
            db.session.commit()
            return "", 204


if __name__ == '__main__':
    app.run(debug=True)
