from flask import Flask, redirect, render_template, request, jsonify, make_response
from flask_restful import Api
from werkzeug.exceptions import abort
from forms.user import LoginForm, RegisterForm
from data import db_session, jobs_api
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from datetime import datetime
from forms.job import JobForm
from forms.department import DepartmentForm
import users_resource
import jobs_resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("index.html", jobs=jobs)


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title='Добавление работы',
                           form=form, title1='Добавление работы')


@app.route('/departments')
def departments():
    db_sess = db_session.create_session()
    department = db_sess.query(Department).all()
    return render_template("departments.html", departments=department)


@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = Department()
        department.title = form.title.data
        department.chief = form.chief.data
        department.email = form.email.data
        department.members = form.members.data
        db_sess.add(department)
        db_sess.commit()
        return redirect('/departments')
    return render_template('add_department.html', title='Добавление департамента',
                           form=form, title1='Добавление департамента')


@app.route('/add_department/<int:department_id>', methods=['GET', 'POST'])
@login_required
def edit_department(department_id):
    form = DepartmentForm()
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == department_id).first()
    if not department or current_user.id not in (1, department_id):
        abort(404)
    if form.validate_on_submit():
        department.title = form.title.data
        department.chief = form.chief.data
        department.email = form.email.data
        department.members = form.members.data
        db_sess.commit()
        return redirect('/departments')
    form.title.data = department.title
    form.chief.data = department.chief
    form.email.data = department.email
    form.members.data = department.members
    return render_template('add_department.html',
                           title='Редактирование департамента',
                           form=form,
                           title1='Редактирование департамента'
                           )


@app.route('/department_delete/<int:department_id>', methods=['GET', 'POST'])
@login_required
def department_delete(department_id):
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == department_id).first()
    if department and current_user.id in (1, department_id):
        db_sess.delete(department)
        db_sess.commit()
        return redirect('/departments')
    abort(404)


@app.route('/add_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    form = JobForm()
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not job or current_user.id not in (1, job_id):
        abort(404)
    if form.validate_on_submit():
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.commit()
        return redirect('/')
    form.team_leader.data = job.team_leader
    form.job.data = job.job
    form.work_size.data = job.work_size
    form.collaborators.data = job.collaborators
    form.is_finished.data = job.is_finished
    return render_template('addjob.html',
                           title='Редактирование работы',
                           form=form,
                           title1='Редактирование работы'
                           )


@app.route('/job_delete/<int:job_id>', methods=['GET', 'POST'])
@login_required
def job_delete(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if job and current_user.id in (1, job_id):
        db_sess.delete(job)
        db_sess.commit()
        return redirect('/')
    abort(404)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            modified_date=datetime.now()
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
    api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
    api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:job_id>')
    db_session.global_init("db/mars_explorer.db")
    app.register_blueprint(jobs_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
