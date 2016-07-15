import time

from onedns.clients import one
from onedns.clients import skydns


class OneMonitor(object):
    '''
    Reads events from OpenNebula and activates/deactivates VM domain names
    '''

    def __init__(self, domain, one_kwargs={}, etcd_kwargs={}):
        self._one = one.OneClient(**one_kwargs)
        self._skydns = skydns.SkyDNSClient(domain, etcd_kwargs=etcd_kwargs)

    def update(self):
        for vm in self._one.vms():
            if hasattr(vm.template, 'nics'):
                self._skydns.register(vm)

    def run(self, interval=10):
        while True:
            self.update()
            time.sleep(interval)
