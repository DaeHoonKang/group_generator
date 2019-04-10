# -*- coding: utf-8 -*-
from http import HTTPStatus
from flask import Blueprint, make_response, jsonify, request
from service.group import GroupService
from exceptions.exception import InvalidParams


group_route = Blueprint('group', __name__, url_prefix='/group')


@group_route.route('', methods=['GET'])
def build_group():
    """ 그룹 생성 API """
    try:
        number = int(request.args.get('number'))
        minimum = int(request.args.get('minimum'))
    except Exception:
        raise InvalidParams('The parameters must be a number type')
    groups = GroupService.build_group(number, minimum)
    return make_response(jsonify({'count': len(groups), 'groups': groups}), HTTPStatus.OK)


