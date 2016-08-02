import pytest

import oca
from oca import vm


def test_get_vms(oneclient):
    vms = oneclient.vms()
    assert isinstance(vms, vm.VirtualMachinePool)
    assert len(vms) > 0


def test_get_vm_by_id(oneclient):
    with pytest.raises(TypeError):
        oneclient.get_vm_by_id('asdf')
    vm = oneclient.get_vm_by_id(0)
    assert isinstance(vm, oca.VirtualMachine)
