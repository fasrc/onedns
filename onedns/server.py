from onedns import resolver
from onedns import exception
from onedns.clients import one
from onedns.logger import log


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

    def _get_vm_dns_entries(self, vm):
        entries = {}
        hostname = vm.name
        primary_ip = vm.template.nics[0].ip
        entries[hostname] = primary_ip
        for nic in vm.template.nics[1:]:
            nicname = "{hostname}-{id}".format(hostname=hostname,
                                               id=nic.nic_id)
            entries[nicname] = nic.ip
        return entries

    def add_vm(self, vm):
        self._check_for_networks(vm)
        dns_entries = self._get_vm_dns_entries(vm)
        log.info("Adding VM {id}: {vm}".format(id=vm.id, vm=vm.name))
        for name, ip in dns_entries.items():
            self.add_host(name, ip)

    def remove_vm(self, vm):
        self._check_for_networks(vm)
        dns_entries = self._get_vm_dns_entries(vm)
        log.info("Removing VM {id}: {vm}".format(id=vm.id, vm=vm.name))
        for name, ip in dns_entries.items():
            self.remove_host(name, ip)

    def add_vm_by_id(self, vm_id):
        vm = self._one.get_vm_by_id(vm_id)
        return self.add_vm(vm)

    def remove_vm_by_id(self, vm_id):
        vm = self._one.get_vm_by_id(vm_id)
        return self.remove_vm(vm)

    def sync(self):
        vms = self._one.vms()
        self.clear()
        for vm in vms:
            try:
                self.add_vm(vm)
            except exception.NoNetworksError as e:
                e.log(warn=True)
