import mock

import pytest

from testfixtures import LogCapture

from onedns import exception
from onedns.tests import vcr
from onedns.tests import utils


def _get_vm_with_nics(one_dns, vms):
    for vm in vms:
        try:
            one_dns._check_for_networks(vm)
            return vm
        except exception.NoNetworksError:
            continue


def _add_and_verify(one_dns, vm, by_id=False, dns_entries=None):
    if by_id:
        one_dns.add_vm_by_id(vm)
    else:
        one_dns.add_vm(vm)
    dns_entries = dns_entries or one_dns._get_vm_dns_entries(vm)
    utils.verify_vm_dns(dns_entries)


def test_onedns_sync(one_dns, vms):
    one_dns.sync(vms=vms)
    uniq_names = []
    uniq_ips = []
    for vm in vms:
        try:
            dns_entries = one_dns._get_vm_dns_entries(vm)
        except exception.NoNetworksError:
            continue
        if vm.name not in uniq_names:
            for name, ip in dns_entries.items():
                dns_entry = {name: ip}
                if ip not in uniq_ips:
                    uniq_ips.append(ip)
                    utils.verify_vm_dns(dns_entry)
                else:
                    with pytest.raises(AssertionError):
                        utils.verify_vm_dns(dns_entry)
            uniq_names.append(vm.name)
        else:
            with pytest.raises(AssertionError):
                utils.verify_vm_dns(dns_entries)


def test_onedns_add_vm(one_dns, vms):
    vm = _get_vm_with_nics(one_dns, vms)
    _add_and_verify(one_dns, vm)


def test_onedns_remove_vm(one_dns, vms):
    vm = _get_vm_with_nics(one_dns, vms)
    dns_entries = one_dns._get_vm_dns_entries(vm)
    _add_and_verify(one_dns, vm)
    one_dns.remove_vm(vm)
    utils.verify_vm_dns_absent(dns_entries)


@vcr.use_cassette()
def test_onedns_add_vm_by_id(oneclient, one_dns):
    vms = oneclient.vms()
    vm = _get_vm_with_nics(one_dns, vms)
    dns_entries = one_dns._get_vm_dns_entries(vm)
    _add_and_verify(one_dns, vm.id, by_id=True, dns_entries=dns_entries)


@vcr.use_cassette()
def test_onedns_remove_vm_by_id(oneclient, one_dns):
    vms = oneclient.vms()
    vm = _get_vm_with_nics(one_dns, vms)
    dns_entries = one_dns._get_vm_dns_entries(vm)
    _add_and_verify(one_dns, vm)
    one_dns.remove_vm_by_id(vm.id)
    utils.verify_vm_dns_absent(dns_entries)


def test_onedns_daemon_no_crash(one_dns):
    def sync_fail(*args, **kwargs):
        raise Exception('this should be logged')
    with LogCapture() as log_capture:
        with mock.patch.object(one_dns, 'sync', sync_fail):
            one_dns.daemon(test=True, sync_interval=1)
        log_capture.check(
            ('onedns', 'ERROR', 'onedns sync failed:')
        )
