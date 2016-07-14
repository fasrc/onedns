import etcd

from onedns.logger import log


class SkyDNSClient(object):
    def __init__(self, etcd_kwargs={}):
        self._etcd = etcd.Client(**etcd_kwargs)

    def register(self, vm):
        log.info("Registering VM: {vm}".format(vm=vm))
