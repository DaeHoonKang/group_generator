# -*- coding: utf-8 -*-
import yaml
import sys
import time
import logging.config
import traceback
from http import HTTPStatus
from absl import flags
from flask import Flask, g, request, make_response, jsonify
from initialize.logging_config import logging_config
from exceptions.exception import InvalidParams, InvalidPerson
from route.person import person_route
from route.group import group_route
from service.person import person_service


flags.DEFINE_string("config", "config.yaml", "config file")
flags.DEFINE_boolean("debug", False, "if debug is true, flask debug mode on")


def create_app(config):
    # global flask app
    app = Flask(__name__)
    # register person route
    app.register_blueprint(person_route)
    # register group route
    app.register_blueprint(group_route)
    # register before request
    @app.before_request
    def before_request():
        g.start = time.time()
    # register after request
    @app.after_request
    def after_request(response):
        now = time.time()
        duration = round(now - g.start, 4)
        remote_addr = request.headers.get('X-Forwarded-For', request.remote_addr)
        host = request.host.split(':', 1)[0]

        log_params = [('method', request.method),
                      ('path', request.path),
                      ('status', response.status_code),
                      ('duration', duration),
                      ('remote', remote_addr),
                      ('host', host)]

        request_id = request.headers.get('X-Request-ID')
        if request_id:
            log_params.append(('request_id', request_id))

        message = []
        for name, value in log_params:
            message.append('{}={}'.format(name, value))
        message = ' '.join(message)
        logging.getLogger('werkzeug').info(message)

        return response

    # register exceptions
    @app.errorhandler(InvalidParams)
    def handle_invalid_params(error):
        logging.getLogger('werkzeug').error(error.to_dict())
        logging.getLogger('werkzeug').error(traceback.format_exc())
        # make reason
        return make_response(jsonify(error.to_dict()), error.status_code)

    @app.errorhandler(InvalidPerson)
    def handle_invalid_params(error):
        logging.getLogger('werkzeug').error(error.to_dict())
        logging.getLogger('werkzeug').error(traceback.format_exc())
        # make reason
        return make_response(jsonify(error.to_dict()), error.status_code)

    @app.errorhandler(Exception)
    def handle_invalid_params(error):
        logging.getLogger('werkzeug').error(error)
        logging.getLogger('werkzeug').error(traceback.format_exc())
        return make_response(jsonify({'reason': 'internal server error'}),
                             HTTPStatus.INTERNAL_SERVER_ERROR)

    return app


def insert_sample_person(number_of_person):
    for num in range(0, number_of_person):
        person_service.insert('Person_{}'.format(num))


if __name__ == "__main__":
    args = flags.FLAGS
    args(sys.argv)

    with open(args.config, 'r') as stream:
        try:
            # load config yaml
            config = yaml.load(stream, Loader=yaml.FullLoader)
            # initialize logging
            logging.config.dictConfig(logging_config)
            # create flask app
            app = create_app(config)
            # insert sample persons
            insert_sample_person(config['data']['num_person'])
            # run flask app
            app.run(debug=args.debug,
                    host=config['run']['host'],
                    port=config['run']['port'])
        except Exception as e:
            print(e)
