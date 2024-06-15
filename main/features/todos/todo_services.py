from flask import session

from main import db
from main.features.todos.todo_models import Todo


class TodoServices:
    @staticmethod
    def add_todo(todo):
        db.session.add(todo)
        db.session.commit()

    @staticmethod
    def todo_list(user_id):
        return Todo.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_todo(todo_id):
        return Todo.query.filter_by(id=todo_id).first()

    @staticmethod
    def delete_todo(todo_id):
        todo = Todo.query.get(todo_id)
        if todo and todo.user_id == session['user']['userinfo']['sub']:
            db.session.delete(todo)
            db.session.commit()

    @staticmethod
    def update_todo(todo):
        db.session.merge(todo)
        db.session.commit()
