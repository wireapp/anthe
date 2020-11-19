import logging

from flask import jsonify
from flask_restx import Namespace, Resource, fields

from wire_flask.Metrics import metrics

status_api = Namespace('service')

logger = logging.getLogger(__name__)


@status_api.route('status', methods=['GET'])
class Status(Resource):
    status = status_api.model('ServiceStatus', {
        'status': fields.String(required=True, description='Indication of service\'s health.', enum=['OK', 'Failing'])
    })

    @metrics.do_not_track()
    @status_api.response(code=200, model=status, description="Returns ok if service is healthy.")
    def get(self):
        return jsonify({'status': 'OK'})


@status_api.route('log', methods=['GET'])
class Status(Resource):

    @metrics.do_not_track()
    @status_api.response(code=200, description='Logs different levels to the application log.')
    def get(self):
        logger.info('Logging info')
        logger.debug('Logging debug')
        logger.warning('Logging warning')
        logger.error('Logging error')
        return jsonify({'status': 'logged'})
