from flask_restx import Resource, Namespace
from flask import request
from models import Movie, MovieSchema
from setup_db import db


movie_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route('/')
class MovieView(Resource):
    def get(self):
        all_movie = db.session.query(Movie).all()

        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        year = request.args.get('year')

        if director_id is not None:
            all_movie = db.session.query(Movie).filter(Movie.director_id == director_id).all()

        if genre_id is not None:
            all_movie = db.session.query(Movie).filter(Movie.genre_id == genre_id).all()

        if year is not None:
            all_movie = db.session.query(Movie).filter(Movie.year == year).all()

        return movies_schema.dump(all_movie), 200

    def post(self):
        data_json = request.json
        new_movie = Movie(**data_json)
        db.session.add(new_movie)
        db.session.commit()
        return '', 201


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        try:
            movie = db.session.query(Movie).filter(Movie.id == mid).one()
            return movie_schema.dump(movie), 200
        except Exception as e:
            return {'error': f'{e}'}, 404

    def put(self, mid):
        try:
            data_json = request.json
            movie_to_update = db.session.query(Movie).filter(Movie.id == mid).one()
            movie_to_update.title = data_json['title']
            movie_to_update.description = data_json['description']
            movie_to_update.trailer = data_json['trailer']
            movie_to_update.year = data_json['year']
            movie_to_update.rating = data_json['rating']
            movie_to_update.genre_id = data_json['genre_id']
            movie_to_update.director_id = data_json['director_id']
            db.session.commit()
            return '', 204
        except Exception as e:
            return {'error': f'{e}'}, 404

    def delete(self, mid):
        try:
            movie_to_delete = db.session.query(Movie).filter(Movie.id == mid).one()
            db.session.delete(movie_to_delete)
            db.session.commit()
            return '', 204
        except Exception as e:
            return {'error': f'{e}'}, 404
