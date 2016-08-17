import dnslib
from dnslib import dns

from IPy import IP

from onedns import utils
from onedns import exception


class Zone(object):
    def __init__(self, domain):
        self.domain = domain
        self._forward = {}
        self._reverse = {}

    def clear(self):
        self._forward = {}
        self._reverse = {}

    def _get_fqdn(self, name):
        return utils.get_fqdn(name, self.domain)

    def _get_rr(self, rname, rtype, rdata):
        return dnslib.RR(rname=dnslib.DNSLabel(rname),
                         rtype=dnslib.QTYPE.reverse[rtype],
                         rclass=dnslib.CLASS.reverse['IN'],
                         rdata=getattr(dns, rtype)(rdata))

    def _add_forward(self, name, ip):
        self._forward[self._get_fqdn(name)] = IP(ip)

    def _get_forward(self, name, ip=None):
        fqdn = self._get_fqdn(name)
        fip = self._forward.get(fqdn)
        if not fip or (ip and fip != IP(ip)):
            raise exception.RecordDoesNotExist(name, ip)
        return fip

    def _remove_forward(self, name, ip=None):
        self._get_forward(name, ip)
        del self._forward[self._get_fqdn(name)]

    def _add_reverse(self, ip, name):
        self._reverse[IP(ip)] = self._get_fqdn(name)

    def _get_reverse(self, ip, name=None):
        reverse = self._reverse.get(IP(ip))
        fqdn = self._get_fqdn(name) if name else None
        if not reverse or (name and fqdn != reverse):
            raise exception.RecordDoesNotExist(ip, fqdn)
        return reverse

    def _remove_reverse(self, ip, name=None):
        self._get_reverse(ip, name)
        del self._reverse[IP(ip)]

    def add_host(self, name, ip):
        self._add_forward(name, ip)
        self._add_reverse(ip, name)

    def remove_host(self, name, ip):
        self._remove_forward(name, ip)
        self._remove_reverse(ip, name)

    def get_forward(self, name):
        fqdn = self._get_fqdn(name)
        forward = self._get_forward(fqdn)
        return self._get_rr(fqdn, 'A', str(forward))

    def get_reverse(self, ip):
        ip = IP(ip)
        reverse = self._get_reverse(ip)
        return self._get_rr(ip.reverseName(), 'PTR', reverse)
