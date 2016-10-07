import logging

from testfixtures import LogCapture

from onedns import logger


def test_onedns_logger():
    assert not logger.log.handlers
    with LogCapture() as log_capture:
        logger.configure_onedns_logging()
        assert logger.log.handlers
        assert logger.console.level == logging.INFO
        logger.log.info('test')
        logger.configure_onedns_logging(debug=True)
        assert logger.console.level == logging.DEBUG
        logger.log.debug('test')
    log_capture.check(
        ('onedns', 'INFO', 'test'),
        ('onedns', 'DEBUG', 'test'),
    )
