# -*- coding: utf-8 -*-
from os.path import dirname, abspath
from app import create_app, insert_sample_person
import unittest
import yaml
import json
import urllib.parse
from http import HTTPStatus
import pprint


class PersonTest(unittest.TestCase):

    def setUp(self):
        path = dirname(dirname(abspath(__file__)))
        with open('{}/config.yaml'.format(path), 'r') as stream:
            try:
                config = yaml.load(stream, Loader=yaml.FullLoader)
                insert_sample_person(config['data']['num_person'])
                self.app = create_app(config).test_client()
            except Exception as e:
                print(e)

    def test_build_group(self):
        print('\r\n==== Build Group ====')
        # 모든 유저 출력
        response = self.app.get('/person')
        print('GET - /person')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = json.loads(response.data)
        pprint.pprint('{}'.format(json.dumps(data, indent=1)))

        # 3그룹 만들기
        query = urllib.parse.urlencode({'number': 3, 'minimum': 1})
        response = self.app.get('/group?{}'.format(query))
        print('GET - /group')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = json.loads(response.data)
        pprint.pprint('{}'.format(json.dumps(data, indent=1)))