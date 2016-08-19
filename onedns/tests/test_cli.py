import pytest

import mock

from onedns import cli
from onedns.tests import test_shell


def test_cli_help():
    with pytest.raises(SystemExit):
        cli.main(args=['--help'])


@mock.patch.object(cli, 'logger', mock.MagicMock())
def test_cli_subcmd_daemon(vms):
    cli.main(args=['daemon'], testing=True, vms=vms)


@mock.patch.dict('sys.modules', test_shell.IPY_MODULES)
@mock.patch.object(cli, 'logger', mock.MagicMock())
def test_cli_subcmd_shell():
    test_shell.IPY.embed.reset_mock()
    cli.main(args=['shell'], testing=True)
    test_shell.IPY.embed.assert_called_once()
