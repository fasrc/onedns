import re
import subprocess
from collections import namedtuple

import oca

RE_VALIDNAME = re.compile('[^\w\d.-]')


VM = namedtuple('VM', 'id, name, running, addr')


class OneClient(object):
    """
    OpenNebula Python client
    """
    def __init__(self, secret=None, address=None, proxy=None):
        self._oca = oca.Client(secret=secret, address=address, proxy=proxy)
        self._vm_pool = oca.VirtualMachinePool(self._oca)

    def vms(self):
        #self._vm_pool.info(filter=-1)
        self._vm_pool.info()
        return self._vm_pool
