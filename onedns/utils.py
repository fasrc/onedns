from onedns.logger import log


def shell(local_ns={}):
    try:
        from IPython import embed
        return embed(user_ns=local_ns)
    except ImportError as e:
        log.error("Unable to load IPython:\n\n%s\n" % e)
        log.error("Please check that IPython is installed and working.")
