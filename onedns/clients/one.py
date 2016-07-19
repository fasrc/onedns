import oca


class OneClient(object):
    """
    OpenNebula Python client
    """
    def __init__(self, secret=None, address=None, proxy=None):
        self._oca = oca.Client(secret=secret, address=address, proxy=proxy)
        self._vm_pool = oca.VirtualMachinePool(self._oca)

    def vms(self):
        self._vm_pool.info(filter=-1)
        return self._vm_pool

    def get_vm_by_id(self, vm_id):
        if type(vm_id) != int or vm_id < 0:
            raise TypeError('vm_id must be an integer >= 0')
        self._vm_pool.info(filter=-1,
                           range_start=vm_id,
                           range_end=vm_id,
                           vm_state=-2)
        return self._vm_pool[0] if self._vm_pool else None
