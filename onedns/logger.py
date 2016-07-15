import os
import logging
import logging.handlers


LOG_FORMAT = ("%(asctime)s %(filename)s:%(lineno)d - %(levelname)s - "
              "%(message)s")


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


def get_onedns_logger():
    log = logging.getLogger('onedns')
    log.addHandler(NullHandler())
    return log


log = get_onedns_logger()
console = logging.StreamHandler()
formatter = logging.Formatter(LOG_FORMAT)
console.setFormatter(formatter)


def configure_onedns_logging(use_syslog=False, syslog_device='/dev/log',
                             debug=False):
    """
    Configure logging for onedns *application* code

    By default onedns's logger has no formatters and a NullHandler so that
    other developers using onedns as a library can configure logging as
    they see fit. This method is used in onedns's application code (i.e.
    the 'onedns' command) to toggle onedns's application specific
    formatters/handlers

    use_syslog - enable logging all messages to syslog. currently only works if
    /dev/log exists on the system (standard for most Linux distros)
    """
    log.setLevel(logging.DEBUG)
    if debug:
        console.setLevel(logging.DEBUG)
    else:
        console.setLevel(logging.INFO)
    log.addHandler(console)
    if use_syslog and os.path.exists(syslog_device):
        log.debug("Logging to %s" % syslog_device)
        syslog_handler = logging.handlers.SysLogHandler(address=syslog_device)
        syslog_handler.setLevel(logging.DEBUG)
        log.addHandler(syslog_handler)
