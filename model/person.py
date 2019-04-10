# -*- coding: utf-8 -*-


class Person:
    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {'name': self.name}

    def __str__(self):
        return self.name