# -*- coding: utf-8 -*-
import random
from model.group import Group
from service.person import person_service
from exceptions.exception import InvalidPerson


class GroupService:
    """
    그룹에 관련된 작업을 처리하는 클래스
    """
    @staticmethod
    def build_group(number, minimum):
        if number is 0 or minimum is 0:
            raise ValueError('The number or minimum fields value is 0')

        persons = person_service.find_all()
        if len(persons) is 0:
            raise InvalidPerson('Persons is empty')

        if len(persons) < number:
            return GroupService.build_minimum_group(persons)

        groups = [Group(name='Group_{}'.format(num)) for num in range(0, number)]
        random.shuffle(persons)
        for index, person in enumerate(persons):
            groups[index % number].append_person(person)

        return {group.name: group.persons for group in groups}

    @staticmethod
    def build_minimum_group(persons):
        group = Group(name='Group_0')
        for person in persons:
            group.append_person(person)
        return {group.name: group.persons}
