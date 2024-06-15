# schema.py
from datetime import datetime

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask import session

from main.features.auth.auth_models import User
from main.features.todos.todo_models import Todo
from main.features.todos.todo_services import TodoServices


class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node,)


class ToDoObject(SQLAlchemyObjectType):
    class Meta:
        model = Todo
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_users = SQLAlchemyConnectionField(UserObject)
    all_todos = SQLAlchemyConnectionField(ToDoObject)

    def resolve_all_todos(self, info):
        user_id = session.get('user', {}).get('id')
        if user_id:
            return Todo.query.filter_by(user_id=user_id).all()
        return []


class CreateToDo(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        time = graphene.String(required=True)
        userId = graphene.String(required=True)

    todo = graphene.Field(lambda: ToDoObject)

    def mutate(self, info, title, description, time):
        user_id = session['user']['userinfo']['sub']
        if not user_id:
            raise Exception("User not authenticated")

        todo = Todo()
        todo.title = title,
        todo.description = description,
        todo.time = datetime.strptime(time, '%Y-%m-%dT%H:%M'),
        todo.user_id = user_id

        todo_services = TodoServices()
        todo_services.add_todo(todo)
        return CreateToDo(todo=todo)


class UpdateToDo(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()
        time = graphene.String()

    todo = graphene.Field(lambda: ToDoObject)

    def mutate(self, info, id, title=None, description=None, time=None):
        user_id = session.get('user', {}).get('id')
        if not user_id:
            raise Exception("User not authenticated")

        todo = Todo.query.get(id)
        if not todo or todo.user_id != user_id:
            raise Exception("To-Do not found or not authorized")

        if title:
            todo.title = title
        if description:
            todo.description = description
        if time:
            todo.time = datetime.strptime(time, '%Y-%m-%dT%H:%M')

        # db.session.commit()
        return UpdateToDo(todo=todo)


class DeleteToDo(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        user_id = session['user']['userinfo']['sub']
        if not user_id:
            raise Exception("User not authenticated")

        todo = Todo.query.get(id)
        if not todo or todo.user_id != user_id:
            raise Exception("To-Do not found or not authorized")

        todo_services = TodoServices()
        todo_services.delete_todo(todo.id)
        return DeleteToDo(ok=True)


class Mutation(graphene.ObjectType):
    create_todo = CreateToDo.Field()
    update_todo = UpdateToDo.Field()
    delete_todo = DeleteToDo.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
