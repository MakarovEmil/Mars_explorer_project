from flask import Flask
from data.db_session import global_init, create_session
from data.users import User
from data.jobs import Jobs
from data.forms.login import LoginForm
from data.forms.registration import RegisterForm
from data.forms.add_job import Adding_Job
from flask_login import LoginManager, login_user, logout_user
from flask import render_template, redirect
from flask_login import login_required
from flask_login import current_user
from flask import request
from flask import abort
from data.api import jobs_api
from flask_restful import Api
from data.api.resources import users_resources, jobs_resources

global_init('Mars/db/mars_explorer.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

api = Api(app)

api.add_resource(users_resources.UsersListResource, '/api/v2/users')
api.add_resource(users_resources.UsersResource, '/api/v2/users/<int:user_id>')

api.add_resource(jobs_resources.JobsListResource, '/api/v2/jobs')
api.add_resource(jobs_resources.JobsResource, '/api/v2/jobs/<int:job_id>')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.get(User, user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    db_sess = create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template('index.html', title='Главная', jobs=jobs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def adding_job():
    form = Adding_Job()
    if form.validate_on_submit():
        db_sess = create_session()
        job = Jobs()
        job.team_leader = form.team_leader_id.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.add(job)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Добавление работы',
                           form=form)


@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = Adding_Job()
    if request.method == "GET":
        db_sess = create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id,
                                         ((Jobs.user == current_user) | (current_user.id == 1))
                                         ).first()
        if job:
            form.job.data = job.job
            form.team_leader_id.data = job.team_leader
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id,
                                         ((Jobs.user == current_user) | (current_user.id == 1))
                                         ).first()
        if job:
            job.team_leader = form.team_leader_id.data
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_job.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id,
                                     ((Jobs.user == current_user) | (current_user.id == 1))
                                     ).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    app.register_blueprint(jobs_api.blueprint)
    app.run(debug=True)


if __name__ == '__main__':
    main()



