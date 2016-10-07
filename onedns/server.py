import re

from onedns import zone
from onedns import resolver
from onedns import exception
from onedns.clients import one
from onedns.logger import log


_BAD_CHARS = re.compile('[^-a-zA-Z0-9]')


class OneDNS(resolver.DynamicResolver):
    """
    This class provides convenience methods for adding/removing VMs to the
    DynamicResolver.
    """

    def __init__(self, domain, one_kwargs={}):
        super(OneDNS, self).__init__(domain)
        self._one = one.OneClient(**one_kwargs)

    def _check_for_networks(self, vm):
        if not hasattr(vm.template, 'nics'):
            raise exception.NoNetworksError(vm)

    def _sanitize_name(self, name):
        name = _BAD_CHARS.sub('-', name)
        return name.strip('-')

    def _get_vm_dns_entries(self, vm):
        self._check_for_networks(vm)
        entries = {}
        hostname = self._sanitize_name(vm.name)
        primary_ip = vm.template.nics[0].ip
        entries[hostname] = primary_ip
        for nic in vm.template.nics[1:]:
            nicname = self._sanitize_name("{hostname}-{id}".format(
                id=nic.nic_id,
                hostname=hostname
            ))
            entries[nicname] = nic.ip
        return entries

    def _check_for_duplicates(self, vm_id, name, ip, zone=None):
        z = zone or self.zone
        try:
            f = z.get_forward(name)
            raise exception.DuplicateVMError(vm_id, f, ip)
        except exception.RecordDoesNotExist:
            pass
        try:
            r = z.get_reverse(ip)
            raise exception.DuplicateVMError(vm_id, ip, r)
        except exception.RecordDoesNotExist:
            pass

    def add_vm(self, vm, zone=None):
        dns_entries = self._get_vm_dns_entries(vm)
        log.info("Adding VM {id}: {vm}".format(id=vm.id, vm=vm.name))
        for name, ip in dns_entries.items():
            self._check_for_duplicates(vm.id, name, ip, zone=zone)
            self.add_host(name, ip, zone=zone)

    def remove_vm(self, vm, zone=None):
        dns_entries = self._get_vm_dns_entries(vm)
        log.info("Removing VM {id}: {vm}".format(id=vm.id, vm=vm.name))
        for name, ip in dns_entries.items():
            self.remove_host(name, ip, zone=zone)

    def add_vm_by_id(self, vm_id):
        vm = self._one.get_vm_by_id(vm_id)
        return self.add_vm(vm)

    def remove_vm_by_id(self, vm_id):
        vm = self._one.get_vm_by_id(vm_id)
        return self.remove_vm(vm)

    def sync(self, vms=None):
        z = zone.Zone(self.domain)
        vms = vms or self._one.vms()
        vms.sort(key=lambda x: x.id)
        for vm in vms:
            try:
                self.add_vm(vm, zone=z)
            except exception.NoNetworksError as e:
                e.log(warn=True)
            except exception.DuplicateVMError as e:
                e.log(warn=True)
        self.load(z)
