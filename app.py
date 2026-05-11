from flask import Flask, render_template, flash, redirect, url_for, session, request, abort
from forms import registerForm, LoginForm, TaskForm
from models import db, User, Task
from flask_bcrypt import Bcrypt
import pandas as pd
import numpy as np
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import os

load_dotenv()
socketio = SocketIO()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    socketio.init_app(app)
    bcrypt = Bcrypt(app)
    bcrypt.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return render_template("home.html")

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                flash('Login successful', 'success')
                session['user_id'] = user.id
                session['username'] = user.username
                return redirect(url_for('dashboard'))
            else:
                flash('Login failed', 'danger')
                return redirect(url_for('login'))
        return render_template("login.html", form=form)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        form = registerForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(
                username = form.username.data,
                email = form.email.data,
                password = hashed_password
            )
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully', 'success')
            return redirect(url_for('login'))
        return render_template("register.html", form=form)

    @app.route('/dashboard')
    def dashboard():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return render_template("dashboard.html")

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        session.pop('username', None)
        flash('You have been logged out!', 'success')
        return redirect(url_for('home'))

    @app.route('/tasks')
    def list_tasks():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        tasks = Task.query.filter_by(user_id=session['user_id']).order_by(Task.id.desc()).all()
        return render_template('task.html', tasks=tasks)

    @app.route('/tasks/new', methods=['GET', 'POST'])
    def create_task():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        form = TaskForm()
        if form.validate_on_submit():
            task = Task(
                title=form.title.data,
                description=form.description.data,
                priority=form.priority.data,
                status=form.status.data,
                user_id=session['user_id'],
                date=form.date.data,
            )
            db.session.add(task)
            db.session.commit()
            socketio.emit('task_update', {
    'message': 'New task created!',
    'title': task.title
})
            flash('Task created successfully.', 'success')
            return redirect(url_for('list_tasks'))
        return render_template('task_form.html', form=form, mode='create')

    @app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
    def edit_task(task_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first()
        if not task:
            abort(404)
        form = TaskForm(obj=task)
        if form.validate_on_submit():
            task.title = form.title.data
            task.description = form.description.data
            task.priority = form.priority.data
            task.status = form.status.data
            task.date = form.date.data
            db.session.commit()
            flash('Task updated successfully.', 'success')
            return redirect(url_for('list_tasks'))
        return render_template('task_form.html', form=form, mode='edit', task=task)


    @app.route('/tasks/<int:task_id>/delete', methods=['POST'])
    def delete_task(task_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first()
        if not task:
            abort(404)
        db.session.delete(task)
        db.session.commit()
        socketio.emit('task_update', {
    'message': 'Task deleted!'
})
        flash('Task deleted successfully.', 'success')
        return redirect(url_for('list_tasks'))
        
    @app.route('/tasks/<int:task_id>/toggle', methods=['POST'])
    def toggle_task(task_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first()
        if not task:
            abort(404)
        task.status = not task.status
        db.session.commit()
        socketio.emit('task_update', {
    'message': 'Task status updated!'
})
        flash('Task status updated.', 'success')
        return redirect(url_for('list_tasks'))

    @app.route('/analytics')
    def analytics():

        if 'user_id' not in session:
            return redirect(url_for('login'))

        tasks = Task.query.filter_by(user_id=session['user_id']).all()

        task_data = []

        for task in tasks:
            task_data.append({
                'title': task.title,
                'status': task.status,
                'priority': task.priority
            })

        df = pd.DataFrame(task_data)

        total_tasks = len(df)

        if total_tasks > 0:
            completed_tasks = np.sum(df['status'] == True)
            pending_tasks = np.sum(df['status'] == False)

            completion_percentage = (
                completed_tasks / total_tasks
            ) * 100
        else:
            completed_tasks = 0
            pending_tasks = 0
            completion_percentage = 0

        return render_template(
            'analytics.html',
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            pending_tasks=pending_tasks,
            completion_percentage=round(completion_percentage, 2)
        )
        
    return app



if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True)