# -*- coding: utf-8 -*-
from http import HTTPStatus
from flask import Blueprint, make_response, jsonify, request
from exceptions.exception import InvalidParams
from utils.functions import json_loads
from service.person import person_service


person_route = Blueprint('person', __name__, url_prefix='/person')


@person_route.route('', methods=['GET'])
def find_all_person():
    """ 모든 Person 조회 API """
    persons = person_service.find_all()
    return make_response(jsonify({'count': len(persons), 'persons': persons}), HTTPStatus.OK)


@person_route.route('', methods=['POST'])
def put_person():
    """ Person 저장 API """
    data = json_loads(request.data)
    name = data.get('name', None)
    if not name:
        raise InvalidParams(reason='One field - name - not found in the json data')
    count = person_service.insert(name)
    return make_response(jsonify({'count': count}), HTTPStatus.OK)


@person_route.route('', methods=['DELETE'])
def delete_person():
    """ Person 삭제 API """
    data = json_loads(request.data)
    name = data.get('name', None)
    if not name:
        raise InvalidParams(reason='One field - name - not found in the json data')
    count = person_service.delete(name)
    return make_response(jsonify({'count': count}), HTTPStatus.OK)
