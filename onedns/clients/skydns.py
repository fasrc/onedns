import re
import json

import etcd

from onedns.logger import log

RE_VALIDNAME = re.compile('[^\w\d.-]')


class SkyDNSClient(object):
    def __init__(self, domain, etcd_kwargs={}):
        self.domain = domain
        self._reverse_domain_parts = domain.split('.')
        self._reverse_domain_parts.reverse()
        self._etcd = etcd.Client(**etcd_kwargs)

    def _skydns_ns(self, parts):
        return '/'.join(['skydns'] +  parts)

    def _get_forward_ns(self, hostname):
        return self._skydns_ns(self._reverse_domain_parts + [hostname])

    def _get_reverse_ns(self, ip):
        ip_parts = ip.split('.')
        return self._skydns_ns(['arpa/in-addr'] + ip_parts)

    def add_forward(self, hostname, ip):
        forward = self._get_forward_ns(hostname)
        log.debug("forward path: {path}".format(path=forward))
        self._etcd.write(forward, json.dumps(dict(host=ip)))

    def add_reverse(self, ip, hostname):
        reverse = self._get_reverse_ns(ip)
        fqdn = '.'.join([hostname, self.domain])
        log.debug("reverse path: {path}".format(path=reverse))
        self._etcd.write(reverse, json.dumps(dict(host=fqdn)))

    def add_host(self, hostname, ip):
        self.add_forward(hostname, ip)
        self.add_reverse(ip, hostname)

    def register(self, vm):
        log.info("Registering VM: {vm}".format(vm=vm.name))
        hostname = RE_VALIDNAME.sub('', vm.name).rstrip('.')
        primary_ip = vm.template.nics[0].ip
        self.add_host(hostname, primary_ip)
        for nic in vm.template.nics[1:]:
            nicname = "{hostname}-{id}".format(hostname=hostname, id=nic.nic_id)
            self.add_host(nicname, nic.ip)
