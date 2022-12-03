from flask_restx import Resource, Namespace
from setup_db import db
from models import Director, DirectorSchema


director_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        all_director = db.session.query(Director).all()
        return directors_schema.dump(all_director), 200


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did):
        try:
            director = db.session.query(Director).filter(Director.id == did).one()
            return director_schema.dump(director), 200
        except Exception as e:
            return {'error': f'{e}'}, 404
