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


class RecordDoesNotExist(OneDnsException):
    """
    Raised when a zone record does not exist
    """
    def __init__(self, key, val=None):
        self.msg = "Record Does Not Exist: {}".format(key)
        if val is not None:
            self.msg += " -> {}".format(val)


class DuplicateVMError(OneDnsException):
    """
    Raised when two or more VMs share a name or IP
    """
    def __init__(self, vmid, key, val):
        self.msg = "VM one-{} has a duplicate: {} -> {}".format(vmid, key, val)
