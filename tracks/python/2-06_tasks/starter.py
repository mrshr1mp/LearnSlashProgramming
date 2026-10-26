"""tasks: a tiny todo list that can save itself."""
import json


class TaskList:
    def __init__(self):
        raise NotImplementedError

    def add(self, title, priority=1):
        raise NotImplementedError

    def done(self, task_id):
        raise NotImplementedError

    def pending(self):
        raise NotImplementedError

    # TODO: make len(task_list) work

    def save(self, path):
        raise NotImplementedError

    @classmethod
    def load(cls, path):
        raise NotImplementedError
