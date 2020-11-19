import logging

from prometheus_flask_exporter import PrometheusMetrics

logger = logging.getLogger(__name__)

metrics = PrometheusMetrics(app=None)

errors_logged = metrics.info('errors_logged', 'Number of logged errors.')
errors_logged.set(0)

warnings_logged = metrics.info('warnings_logged', 'Number of logged warnings.')
warnings_logged.set(0)


def init_metrics(app, version, application_name):
    """
    Initialize metrics.
    """
    metrics.init_app(app)
    metrics.info('application', application_name, version=version)
