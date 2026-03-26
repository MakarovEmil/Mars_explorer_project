from flask import jsonify
from flask_restful import abort, Resource
from ... import db_session
from ...users import User
from .arg_parser_users import parser


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"Users {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        users = db_sess.get(User, user_id)
        return jsonify({'users': users.to_dict()})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.get(User, user_id)
        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        users = db_sess.get(User, user_id)
        args = parser.parse_args()
        users.surname = args['surname']
        users.name = args['name']
        users.age = args['age']
        users.position = args['position']
        users.speciality = args['speciality']
        users.address = args['address']
        users.email = args['email']
        users.set_password(args['password'])
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify({
            'users': [item.to_dict() for item in users]
        })

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        users = User(
            surname = args['surname'],
            name = args['name'],
            age = args['age'],
            position = args['position'],
            speciality = args['speciality'],
            address = args['address'],
            email = args['email']
        )
        users.set_password(args['password'])
        db_sess.add(users)
        db_sess.commit()
        return jsonify({'id': users.id})


