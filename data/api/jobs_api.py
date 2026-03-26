from flask import make_response, jsonify, request
from flask import Blueprint
from .. import db_session
from ..jobs import Jobs


blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)

db_session.global_init('db/mars_explorer.db')


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'work_size', 'is_finished', 'collaborators']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    elif type(request.json['is_finished']) != bool:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    jobs = Jobs(
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        work_size=request.json['work_size'],
        is_finished=request.json['is_finished'],
        collaborators=request.json['collaborators']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'id': jobs.id})


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'jobs':
                [item.to_dict()
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_job(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.get(Jobs, jobs_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def edit_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.get(Jobs, jobs_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    elif not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'work_size', 'is_finished', 'collaborators']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    elif type(request.json['is_finished']) != bool:
        return make_response(jsonify({'error': 'Bad request'}), 400)

    jobs.job = request.json['job']
    jobs.team_leader = request.json['team_leader']
    jobs.work_size = request.json['work_size']
    jobs.is_finished = request.json['is_finished']
    jobs.collaborators = request.json['collaborators']
    db_sess.commit()
    return jsonify({'success': 'OK'})