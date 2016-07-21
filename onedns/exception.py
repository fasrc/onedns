from onedns.logger import log


class OneDnsException(Exception):
    def __init__(self, *args):
        self.args = args
        self.msg = args[0]

    def __str__(self):
        return self.msg

    def explain(self):
        return '%s: %s' % (self.__class__.__name__, self.msg)

    def log(self, warn=False, show_tb=False):
        if warn:
            log.warn(self.explain(), exc_info=show_tb)
        else:
            log.error(self.explain(), exc_info=show_tb)


class NoNetworksError(OneDnsException):
    """
    Raised when a VM doesn't have any NICs
    """
    def __init__(self, vm):
        self.msg = "No networks found for VM {id}: {vm}".format(vm=vm.name,
                                                                id=vm.id)
