import logging

logger = logging.getLogger(__name__)


def log_action(action, user=None, details=None):
    logger.info('ACTION %s user=%s details=%s', action, getattr(user, 'id', None), details or {})


def log_error(exc, request=None, user=None):
    logger.exception('ERROR %s user=%s path=%s', exc, getattr(user, 'id', None), getattr(request, 'path', None))
