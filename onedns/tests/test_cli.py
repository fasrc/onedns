import pytest

import mock

from onedns import cli
from onedns.tests import test_shell


def test_cli_help():
    with pytest.raises(SystemExit):
        cli.main(args=['--help'])


@mock.patch.object(cli, 'logger', mock.MagicMock())
def test_cli_subcmd_daemon(vms):
    cli.main(args='daemon --dns-port 9053 --sync-interval 1'.split(),
             test=True, test_vms=vms)


@mock.patch.dict('sys.modules', test_shell.IPY_MODULES)
@mock.patch.object(cli, 'logger', mock.MagicMock())
def test_cli_subcmd_shell():
    test_shell.IPY.embed.reset_mock()
    cli.main(args=['shell'], test=True)
    test_shell.IPY.embed.assert_called_once()


def test_invalid_values():
    with pytest.raises(SystemExit):
        cli.main(args='daemon --dns-port asdf'.split())
    with pytest.raises(SystemExit):
        cli.main(args='daemon --dns-port 0'.split())
    with pytest.raises(SystemExit):
        cli.main(args='daemon --sync-interval asdf'.split())
    with pytest.raises(SystemExit):
        cli.main(args='daemon --sync-interval 0'.split())
