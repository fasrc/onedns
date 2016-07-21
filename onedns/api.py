from onedns.clients import one
from onedns.clients import skydns
from onedns.logger import log


class OneDNS(object):
    """
    This class bridges the gap between OpenNebula and SkyDNS APIs. It primarily
    provides convenience methods for adding/removing VMs to SkyDNS.
    """

    def __init__(self, domain, one_kwargs={}, etcd_kwargs={}):
        self._one = one.OneClient(**one_kwargs)
        self._skydns = skydns.SkyDNSClient(domain, etcd_kwargs=etcd_kwargs)

    def _get_vm_dns_entries(self, vm):
        entries = {}
        if not hasattr(vm.template, 'nics'):
            return entries
        hostname = vm.name
        primary_ip = vm.template.nics[0].ip
        entries[hostname] = primary_ip
        for nic in vm.template.nics[1:]:
            nicname = "{hostname}-{id}".format(hostname=hostname,
                                               id=nic.nic_id)
            entries[nicname] = nic.ip
        return entries

    def add_vm(self, vm):
        dns_entries = self._get_vm_dns_entries(vm)
        if not dns_entries:
            log.warn("No networks found for VM {id}: {vm} - skipping".format(
                vm=vm.name, id=vm.id))
            return
        log.info("Adding VM {id}: {vm}".format(id=vm.id, vm=vm.name))
        for name, ip in dns_entries.items():
            self._skydns.add_host(name, ip)

    def remove_vm(self, vm):
        dns_entries = self._get_vm_dns_entries(vm)
        if not dns_entries:
            log.warn("No networks found for VM {id}: {vm} - skipping".format(
                vm=vm.name, id=vm.id))
            return
        log.info("Removing VM {id}: {vm}".format(id=vm.id, vm=vm.name))
        for name, ip in dns_entries.items():
            self._skydns.remove_host(name, ip)

    def add_vm_by_id(self, vm_id):
        vm = self._one.get_vm_by_id(vm_id)
        return self.add_vm(vm)

    def remove_vm_by_id(self, vm_id):
        vm = self._one.get_vm_by_id(vm_id)
        return self.remove_vm(vm)

    def sync(self):
        for vm in self._one.vms():
            self.add_vm(vm)
