#!/usr/bin/env python3
"""REST API for keep/shared data"""
from __future__ import print_function
from flask_restx import Resource, Namespace
from passnfly.api.dao.todo import TodoDAO
from passnfly.api.aiokafka.todo import post_data2
from passnfly.api.models.todo import api, ns, todo, add_models_to_namespace


todo_ns = Namespace('Todo', description='Operations related to todo')
add_models_to_namespace(todo_ns)

DAO = TodoDAO()

@ns.route('/')
@ns.response(404, 'Todo not found')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''Make a thread for running every 30 sec ping request to kafka'''
        topic=post_data2('ping')
        print("We use topic for ping: " + topic)
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource and make pong'''
        topic=post_data2('pong')
        print("We use topic for pong: " + topic)
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)
