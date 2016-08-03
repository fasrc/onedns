import os

import mock

from onedns import utils


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
