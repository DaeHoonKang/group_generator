# -*- coding: utf-8 -*-


class Group:
    def __init__(self, name):
        self.name = name
        self.persons = []

    def append_person(self, person):
        self.persons.append(person)

    def to_dict(self):
        return {'name': self.name, 'persons': self.persons}

    def __str__(self):
        return '{}:{}'.format(self.name, ','.join(self.persons))