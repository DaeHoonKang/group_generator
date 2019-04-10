# -*- coding: utf-8 -*-
from repository.PersonRepository import PersonRepository
from model.person import Person


class PersonService:
    """
    Person 데이터를 처리하는 클래스
    """
    def __init__(self):
        self.repo = PersonRepository()

    def insert(self, name):
        count = self.repo.insert(person=Person(name=name))
        return count

    def find_all(self):
        persons = self.repo.find()
        return persons

    def delete(self, name):
        count = self.repo.delete(person=Person(name=name))
        return count


person_service = PersonService()