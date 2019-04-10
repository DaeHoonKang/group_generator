# -*- coding: utf-8 -*-
from threading import Lock
from repository.repository import Repository


class PersonRepository(Repository):

    def __init__(self):
        self.__persons = dict()
        self.__lock = Lock()

    def find(self, **kwargs):
        with self.__lock:
            if len(kwargs) is 0:
                return self._find_all()

            name = kwargs.get('name')
            person = self.__persons.get(name, None)
            if not person:
                return []
            return [person.name]

    def _find_all(self):
        return [name for name, person in self.__persons.items()]

    def insert(self, **kwargs):
        with self.__lock:
            person = kwargs.get('person', None)
            if not person:
                return 0

            if person.name in self.__persons:
                return 0

            old = len(self.__persons)
            self.__persons[person.name] = person
            return len(self.__persons) - old

    def delete(self, **kwargs):
        with self.__lock:
            person = kwargs.get('person', None)
            if not person:
                return 0

            old = len(self.__persons)
            if person.name in self.__persons:
                del self.__persons[person.name]

            return old - len(self.__persons)

    def clear(self):
        with self.__lock:
            self.__persons.clear()