import pytest

import dnslib

from IPy import IP

from onedns import exception
from onedns.tests import conftest


def test_zone_clear(onezone):
    assert onezone._forward
    assert onezone._reverse
    onezone.clear()
    assert not onezone._forward
    assert not onezone._reverse


def test_add_host(onezone):
    onezone.clear()
    with pytest.raises(exception.RecordDoesNotExist):
        onezone._get_forward(conftest.HOST_SHORT, conftest.HOST_IP)
    with pytest.raises(exception.RecordDoesNotExist):
        onezone._get_reverse(conftest.HOST_IP, conftest.HOST_SHORT)
    onezone.add_host(conftest.HOST_SHORT, conftest.HOST_IP)
    assert onezone._get_forward(conftest.HOST_SHORT, conftest.HOST_IP)
    assert onezone._get_reverse(conftest.HOST_IP, conftest.HOST_SHORT)


def test_remove_host(onezone):
    onezone.clear()
    onezone.add_host(conftest.HOST_SHORT, conftest.HOST_IP)
    assert onezone._get_forward(conftest.HOST_SHORT, conftest.HOST_IP)
    assert onezone._get_reverse(conftest.HOST_IP, conftest.HOST_SHORT)
    onezone.remove_host(conftest.HOST_SHORT, conftest.HOST_IP)
    with pytest.raises(exception.RecordDoesNotExist):
        onezone._get_forward(conftest.HOST_SHORT, conftest.HOST_IP)
    with pytest.raises(exception.RecordDoesNotExist):
        onezone._get_reverse(conftest.HOST_IP, conftest.HOST_SHORT)


@pytest.mark.parametrize("host", conftest.TEST_GET_FORWARD_DATA)
def test_get_forward(onezone, host):
    forward = onezone.get_forward(host)
    fqdn = conftest.HOST + '.'
    assert isinstance(forward, dnslib.RR)
    assert forward.rname == fqdn
    assert forward.rtype == dnslib.QTYPE.A
    assert forward.rclass == dnslib.CLASS.IN
    assert str(forward.rdata) == conftest.HOST_IP


def test_get_reverse(onezone):
    reverse = onezone.get_reverse(conftest.HOST_IP)
    fqdn = conftest.HOST + '.'
    revip = IP(conftest.HOST_IP).reverseName()
    assert isinstance(reverse, dnslib.RR)
    assert reverse.rname == revip
    assert reverse.rtype == dnslib.QTYPE.PTR
    assert reverse.rclass == dnslib.CLASS.IN
    assert str(reverse.rdata) == fqdn
