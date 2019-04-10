# -*- coding: utf-8 -*-
from os.path import dirname, abspath
from app import create_app
import unittest
import yaml
import json
from http import HTTPStatus


class PersonTest(unittest.TestCase):

    def setUp(self):
        path = dirname(dirname(abspath(__file__)))
        with open('{}/config.yaml'.format(path), 'r') as stream:
            try:
                config = yaml.load(stream, Loader=yaml.FullLoader)
                self.app = create_app(config).test_client()
            except Exception as e:
                print(e)

    def test_put_person(self):
        print('\r\n==== Put Person ====')
        # 이름 저장
        data = json.dumps({'name': '홍길동'})
        response = self.app.post('/person', data=data, content_type='application/json')
        print('POST - /person data={}'.format(data))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 1)
        print('Response - data={}'.format(data))

        # 특수 문자 이름 저장
        data = json.dumps({'name': '#1社Z'})
        response = self.app.post('/person', data=data, content_type='application/json')
        print('POST - /person data={}'.format(data))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 1)
        print('Response - data={}'.format(data))

        # 모든 유저 출력
        response = self.app.get('/person')
        print('GET - /person')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = json.loads(response.data)
        print('Response - data={}'.format(data))

    def test_delete_person(self):
        print('\r\n==== Delete Person ====')
        # 이름 저장
        data = json.dumps({'name': '홍길동'})
        response = self.app.post('/person', data=data, content_type='application/json')
        print('POST - /person data={}'.format(data))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 1)
        print('Response - data={}'.format(data))

        # 이름 삭제
        data = json.dumps({'name': '홍길동'})
        response = self.app.delete('/person', data=data, content_type='application/json')
        print('POST - /person data={}'.format(data))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 1)
        print('Response - data={}'.format(data))

        # 모든 유저 출력
        response = self.app.get('/person')
        print('GET - /person')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = json.loads(response.data)
        print('Response - data={}'.format(data))