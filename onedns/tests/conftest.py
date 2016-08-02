import pytest

from onedns import server


DOMAIN = 'onedns.test'
INTERFACE = '127.0.0.1'
PORT = 9053


@pytest.fixture(scope="function")
def dns(request):
    dns = server.DynamicResolver(domain=DOMAIN)
    dns.start(dns_address=INTERFACE, dns_port=PORT, tcp=True)
    request.addfinalizer(dns.close)
    return dns
