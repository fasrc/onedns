import argparse

from onedns import api
from onedns import utils
from onedns import logger
from onedns import monitor


def daemon(args, one_args):
    mon = monitor.OneMonitor(args.domain, one_kwargs=one_args)
    mon.run(args.interval)


def add_host(args, one_args):
    pass


def remove_host(args, one_args):
    pass


def add_vm(args, one_args):
    client = api.OneDNS(args.domain, one_kwargs=one_args)
    client.add_vm_by_id(args.id)


def remove_vm(args, one_args):
    client = api.OneDNS(args.domain, one_kwargs=one_args)
    client.remove_vm_by_id(args.id)


def shell(args, one_args):
    onemon = monitor.OneMonitor(args.domain, one_kwargs=one_args)
    oneclient = onemon._one
    ns = dict(onemon=onemon, oneclient=oneclient, log=logger.log)
    utils.shell(local_ns=ns)


def main(args=None):
    parser = argparse.ArgumentParser(
        description='OneDNS - Dynamic DNS for OpenNebula')
    parser.add_argument('--debug', required=False,
                        action='store_true', default=False,
                        help='ONE controller host address')
    parser.add_argument('-d', '--domain', required=False, default='one.local',
                        help='DNS domain to use')
    parser.add_argument('--one-address', required=False,
                        help='ONE controller host address')
    parser.add_argument('--one-secret', required=False,
                        help='ONE credentials to use (e.g. user:key)')
    parser.add_argument('--one-proxy', required=False,
                        help='proxy host to use to connect to ONE controller')
    subparsers = parser.add_subparsers()

    daemon_parser = subparsers.add_parser('daemon')
    daemon_parser.set_defaults(func=daemon)
    daemon_parser.add_argument(
        '-i', '--interval', required=False, type=int, default=60,
        help="how often in seconds to poll ONE and update DNS")

    add_parser = subparsers.add_parser('add')
    add_subparser = add_parser.add_subparsers()

    add_vm_parser = add_subparser.add_parser('vm')
    add_vm_parser.set_defaults(func=add_vm)
    add_vm_parser.add_argument('id', type=int, help='id of the vm to add')

    add_host_parser = add_subparser.add_parser('host')
    add_host_parser.set_defaults(func=add_host)
    add_host_parser.add_argument('hostname', help='name of host to add')
    add_host_parser.add_argument('ip', help='ip of host to add')

    rm_parser = subparsers.add_parser('remove')
    rm_subparser = rm_parser.add_subparsers()

    rm_vm_parser = rm_subparser.add_parser('vm')
    rm_vm_parser.set_defaults(func=remove_vm)
    rm_vm_parser.add_argument('id', type=int, help='id of the vm to add')

    rm_host_parser = rm_subparser.add_parser('host')
    rm_host_parser.set_defaults(func=remove_host)
    rm_host_parser.add_argument('hostname', help='name of host to remove')
    rm_host_parser.add_argument('ip', help='ip of host to remove')

    shell_parser = subparsers.add_parser('shell')
    shell_parser.set_defaults(func=shell)

    args = parser.parse_args(args=args)

    logger.configure_onedns_logging(debug=args.debug)

    args_dict = vars(args)
    one_args = utils.get_kwargs_from_dict(args_dict, 'one_')

    args.func(args, one_args)
