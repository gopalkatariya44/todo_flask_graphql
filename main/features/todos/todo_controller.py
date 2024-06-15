import os
import uuid
from datetime import datetime

from flask import Blueprint, session, url_for, redirect, request, render_template, current_app
from werkzeug.utils import secure_filename

from main import settings
from main.features.auth.auth_services import AuthServices
from main.features.todos.todo_models import Todo
from main.features.todos.todo_services import TodoServices

router = Blueprint('todos', __name__)


@router.route('/', methods=['GET', 'POST'])
def home():
    todo_services = TodoServices()
    auth_services = AuthServices()
    if "user" not in session:
        return redirect(url_for("auth.loginr"))
    user_id = session['user']['userinfo']['sub']
    todos = todo_services.todo_list(user_id)
    user = auth_services.get_user(user_id)
    return render_template("todos/home.html", todos=todos, is_pro=user.is_pro,
                           stripe_public_key=settings.STRIPE_PUBLIC_KEY)


@router.route('/todo/add', methods=['POST'])
def add_todo():
    todo_services = TodoServices()

    user_id = session['user']['userinfo']['sub']
    title = request.form.get('title')
    description = request.form.get('description')
    time = request.form.get('time')
    image = request.files.get('image')

    if image:
        filename = secure_filename(image.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        os.makedirs(current_app.config['UPLOAD_FOLDER'] + f"/{user_id}", exist_ok=True)
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], user_id, unique_filename))
        image_path = unique_filename  # Save the filename or the relative path to the database
    else:
        image_path = None

    todo = Todo()
    todo.user_id = user_id
    todo.title = title
    todo.description = description
    todo.time = datetime.strptime(time, '%Y-%m-%dT%H:%M')
    todo.img_url = image_path

    todo_services.add_todo(todo)

    return redirect(url_for('todos.home'))


@router.route('/todos/delete/<todo_id>', methods=['POST'])
def delete_todo(todo_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    todo_services = TodoServices()
    todo_services.delete_todo(todo_id)

    return redirect(url_for('todos.home'))


@router.route('/todo/update/<todo_id>', methods=['GET', 'POST'])
def update_todo(todo_id):
    todo_services = TodoServices()

    if request.method == "GET":
        todo = todo_services.get_todo(todo_id)
        print(todo.__dict__)
        formatted_time = todo.time.strftime('%Y-%m-%dT%H:%M')
        return render_template("todos/update_todo.html", todo=todo, formatted_time=formatted_time)

    user_id = session['user']['userinfo']['sub']
    title = request.form.get('title')
    description = request.form.get('description')
    time = request.form.get('time')
    image = request.files.get('image')

    if image:
        filename = secure_filename(image.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        os.makedirs(current_app.config['UPLOAD_FOLDER'] + f"/{user_id}", exist_ok=True)
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], user_id, unique_filename))
        image_path = unique_filename  # Save the filename or the relative path to the database
    else:
        image_path = None

    todo = Todo()
    todo.id = todo_id
    todo.user_id = user_id
    todo.title = title
    todo.description = description
    todo.time = datetime.strptime(time, '%Y-%m-%dT%H:%M')
    todo.img_url = image_path
    print(todo.__dict__)

    todo_services.update_todo(todo)

    return redirect(url_for('todos.home'))
