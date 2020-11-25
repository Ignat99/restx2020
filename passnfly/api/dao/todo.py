#!/usr/bin/env python3
""" Main model and classes of RESTX API """
#from __future__ import print_function

class TodoDAO(object):
    """Data Access Object for Program functionalities"""
    def __init__(self):
        """List and counter initialisation"""
        self.counter = 0
        self.todos = []

    def get(self, id1):
        """Full list of objects"""
        for todo in self.todos:
            if todo['id'] == id1:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id1))

    def create(self, data):
        """Create the object and put to list"""
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id1, data):
        """Update the object from list"""
        todo = self.get(id1)
        todo.update(data)
        return todo

    def delete(self, id1):
        """Remove a object from the list"""
        todo = self.get(id1)
        self.todos.remove(todo)
