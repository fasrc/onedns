import os
import logging
import logging.handlers


LOG_FORMAT = ("%(asctime)s %(filename)s:%(lineno)d - %(levelname)s - "
              "%(message)s")

log = logging.getLogger('onedns')
console = logging.StreamHandler()
formatter = logging.Formatter(LOG_FORMAT)
console.setFormatter(formatter)


def configure_onedns_logging(debug=False):
    """
    Configure logging for onedns *application* code

    By default onedns's logger is completely unconfigured so that other
    developers using onedns as a library can configure logging as they see fit.
    This method is used in onedns's application code (i.e.  the 'onedns'
    command) to toggle onedns's application specific formatters/handlers
    """
    log.setLevel(logging.DEBUG)
    if debug:
        console.setLevel(logging.DEBUG)
    else:
        console.setLevel(logging.INFO)
    log.addHandler(console)
