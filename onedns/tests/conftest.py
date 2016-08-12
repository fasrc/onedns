import pytest

from onedns import resolver
from onedns.tests import vcr
from onedns.clients import one


DOMAIN = 'onedns.test'
INTERFACE = '127.0.0.1'
PORT = 9053


@pytest.fixture(scope="function")
def dns(request):
    dns = resolver.DynamicResolver(domain=DOMAIN)
    dns.start(dns_address=INTERFACE, dns_port=PORT, tcp=True)
    request.addfinalizer(dns.close)
    return dns


@pytest.fixture(scope="function")
def oneclient(request):
    """
    NOTE: All fixtures must be function scope to work with VCRPY cassettes
    """
    return one.OneClient()


@pytest.fixture(scope="function")
@vcr.use_cassette()
def vms(oneclient):
    return oneclient.vms()
