from onedns.tests import vcr

import pytest

import oca
from oca import vm


@vcr.use_cassette()
def test_get_vms(oneclient):
    vms = oneclient.vms()
    assert isinstance(vms, vm.VirtualMachinePool)
    assert len(vms) > 0


@vcr.use_cassette()
def test_get_vm_by_id(oneclient):
    with pytest.raises(TypeError):
        oneclient.get_vm_by_id('asdf')
    vm = oneclient.get_vm_by_id(0)
    assert isinstance(vm, oca.VirtualMachine)
