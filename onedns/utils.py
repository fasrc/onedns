from onedns.logger import log


def get_kwargs_from_dict(d, prefix):
    kwargs = dict((i.replace(prefix, ''), d[i])
                  for i in d.keys() if i.startswith(prefix))
    return kwargs


def shell(local_ns={}):
    try:
        from IPython import embed
        return embed(user_ns=local_ns)
    except ImportError as e:
        log.error("Unable to load IPython:\n\n%s\n" % e)
        log.error("Please check that IPython is installed and working.")
