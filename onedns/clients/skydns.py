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

    def _sanitize_name(self, name):
        return RE_VALIDNAME.sub('', name).rstrip('.')

    def _skydns_ns(self, parts):
        return '/'.join(['skydns'] + parts)

    def _get_forward_ns(self, hostname):
        return self._skydns_ns(self._reverse_domain_parts + [hostname])

    def _get_reverse_ns(self, ip):
        ip_parts = ip.split('.')
        return self._skydns_ns(['arpa/in-addr'] + ip_parts)

    def add_forward(self, hostname, ip):
        forward = self._get_forward_ns(hostname)
        log.debug("adding forward: {path}".format(path=forward))
        self._etcd.write(forward, json.dumps(dict(host=ip)))

    def remove_forward(self, hostname):
        forward = self._get_forward_ns(hostname)
        log.debug("removing forward: {path}".format(path=forward))
        self._etcd.delete(forward)

    def add_reverse(self, ip, hostname):
        reverse = self._get_reverse_ns(ip)
        fqdn = '.'.join([hostname, self.domain])
        log.debug("adding reverse: {path}".format(path=reverse))
        self._etcd.write(reverse, json.dumps(dict(host=fqdn)))

    def remove_reverse(self, ip):
        reverse = self._get_reverse_ns(ip)
        log.debug("removing reverse: {path}".format(path=reverse))
        self._etcd.delete(reverse)

    def add_host(self, hostname, ip):
        hostname = self._sanitize_name(hostname)
        self.add_forward(hostname, ip)
        self.add_reverse(ip, hostname)

    def remove_host(self, hostname, ip):
        hostname = self._sanitize_name(hostname)
        self.remove_forward(hostname)
        self.remove_reverse(ip)
