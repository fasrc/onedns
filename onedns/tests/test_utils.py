import os

import mock
import pytest

from onedns import utils
from onedns.tests import conftest


ONE_XMLRPC = 'https://controller:2633/RPC2'


def test_get_kwargs_from_dict():
    d = dict(ONE_XMLRPC=ONE_XMLRPC)
    kwargs = utils.get_kwargs_from_dict(d, prefix='ONE_')
    assert kwargs['XMLRPC'] == ONE_XMLRPC
    kwargs = utils.get_kwargs_from_dict(d, prefix='ONE_', lower=True)
    assert kwargs['xmlrpc'] == ONE_XMLRPC


@mock.patch.dict(os.environ, {'ONE_XMLRPC': ONE_XMLRPC})
def test_get_kwargs_from_env():
    kwargs = utils.get_kwargs_from_env(prefix='ONE_')
    assert kwargs['XMLRPC'] == ONE_XMLRPC
    kwargs = utils.get_kwargs_from_env(prefix='ONE_', lower=True)
    assert kwargs['xmlrpc'] == ONE_XMLRPC


@pytest.mark.parametrize("name,domain", conftest.TEST_FQDN_DATA)
def test_get_fqdn(name, domain):
    fqdn = utils.get_fqdn(name, domain)
    assert fqdn == conftest.TEST_FQDN_RESULT
