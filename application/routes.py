from flask import current_app as app, request
from flask_restx import Api, Namespace, Resource

from application.models import db
from application import models, schema
import data


api: Api = app.config['api']
movies_ns: Namespace = api.namespace('movies')
director_ns = api.namespace('director')
genre_ns = api.namespace('genre')

movie_schema = schema.Movie()
movies_schema = schema.Movie(many=True)

director_schema = schema.Director()
directors_schema = schema.Director(many=True)

genre_schema = schema.Genre()
genres_schema = schema.Genre(many=True)


@movies_ns.route('/')
class MoviesView(Resource):

    def get(self):
        movies_query = db.session.query(models.Movie)
        args = request.args
        director_id = args.get('director_id')
        if director_id is not None:
            movies_query = movies_query.filter(models.Movie.director_id == director_id)

        genre_id = args.get('genre_id')
        if genre_id is not None:
            movies_query = movies_query.filter(models.Movie.genre_id == genre_id)

        movies = movies_query.all()

        return movies_schema.dump(movies), 200

    def post(self):
        req_json = request.json
        new_movie = models.Movie(**req_json)
        db.session.add(new_movie)
        db.session.commit()

        return {}, 201


@movies_ns.route('/<int:movie_id>')
class MoviesView(Resource):

    def get(self, movie_id):
        movie = db.session.query(models.Movie).filter(models.Movie.id == movie_id).first()
        if movie is None:

            return {}, 404
        return movie_schema.dump(movie), 200

    def put(self, movie_id):
        db.session.query(models.Movie).filter(models.Movie.id == movie_id).update(request.json)
        db.session.commit()

        return None, 204

    def delete(self, movie_id):
        db.session.query(models.Movie).filter(models.Movie.id == movie_id).delete()
        db.session.commit()

        return None, 204


@director_ns.route('/<int:director_id>')
class DirectotView(Resource):

    def get(self, director_id):
        director = db.session.query(models.Director).filter(models.Director.id == director_id).first()

        if director is None:
            return {}, 404

        return director_schema.dump(director), 200


@director_ns.route('/')
class DirectorsView(Resource):

    def get(self):
        directors = db.session.query(models.Director).all()

        return directors_schema.dump(directors), 200


@genre_ns.route('/<int:genre_id>')
class GenreView(Resource):

    def get(self, genre_id):
        genre = db.session.query(models.Genre).filter(models.Genre.id == genre_id).first()

        if genre is None:
            return {}, 404

        return genre_schema.dump(genre), 200


@genre_ns.route('/')
class GenresView(Resource):

    def get(self):
        genres = db.session.query(models.Genre).all()

        return genres_schema.dump(genres), 200