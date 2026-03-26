from flask import jsonify
from flask_restful import abort, Resource
from ... import db_session
from ...jobs import Jobs
from .arg_parser_jobs import parser


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    if not jobs:
        abort(404, message=f"Users {job_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        db_sess = db_session.create_session()
        jobs = db_sess.get(Jobs, job_id)
        return jsonify({'jobs': jobs.to_dict()})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        db_sess = db_session.create_session()
        jobs = db_sess.get(Jobs, job_id)
        db_sess.delete(jobs)
        db_sess.commit()
        return jsonify({'success': 'OK'})

    def put(self, job_id):
        abort_if_job_not_found(job_id)
        db_sess = db_session.create_session()
        jobs = db_sess.get(Jobs, job_id)
        args = parser.parse_args()
        jobs.team_leader = args['team_leader']
        jobs.job = args['job']
        jobs.work_size = args['work_size']
        jobs.collaborators = args['collaborators']
        jobs.is_finished = args['is_finished']
        db_sess.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).all()
        return jsonify({
            'jobs': [item.to_dict() for item in jobs]
        })

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        jobs = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished']
        )
        db_sess.add(jobs)
        db_sess.commit()
        return jsonify({'id': jobs.id})