import argparse

from onedns import monitor
from onedns import utils
from onedns import logger
from onedns.clients import skydns


def get_kwargs(args, prefix):
    args_dict = vars(args)
    one_args = dict((i.replace(prefix, ''), args_dict[i])
                    for i in args_dict.keys() if i.startswith(prefix))
    return one_args


def daemon(args, one_args, etcd_args):
    mon = monitor.OneMonitor(args.domain, one_kwargs=one_args,
                             etcd_kwargs=etcd_args)
    mon.run(args.interval)


def add(args, one_args, etcd_args):
    client = skydns.SkyDNSClient(args.domain, etcd_kwargs=etcd_args)
    client.add_host(args.hostname, args.ip)


def remove(args, one_args, etcd_args):
    client = skydns.SkyDNSClient(args.domain, etcd_kwargs=etcd_args)
    client.remove_host(args.hostname, args.ip)


def shell(args, one_args, etcd_args):
    onemon = monitor.OneMonitor(args.domain, one_kwargs=one_args,
                                etcd_kwargs=etcd_args)
    oneclient = onemon._one
    skyclient = onemon._skydns
    etcdclient = skyclient._etcd
    ns = dict(onemon=onemon, skyclient=skyclient, oneclient=oneclient,
              etcdclient=etcdclient)
    utils.shell(local_ns=ns)


def main():
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
    parser.add_argument('--etcd-host', required=False,
                        help='etcd host to connect to')
    parser.add_argument('--etcd-port', required=False, type=int, default=4001,
                        help='etcd port to connect to')
    parser.add_argument('--etcd-cert', required=False, type=int,
                        help='path to etcd client ssl cert')
    subparsers = parser.add_subparsers()

    daemon_parser = subparsers.add_parser('daemon')
    daemon_parser.set_defaults(func=daemon)
    daemon_parser.add_argument(
        '-i', '--interval', required=False, type=int, default=60,
        help="how often in seconds to poll ONE and update DNS")

    add_parser = subparsers.add_parser('add')
    add_parser.set_defaults(func=add)
    add_parser.add_argument('hostname', help='name of host to add')
    add_parser.add_argument('ip', help='ip of host to add')

    remove_parser = subparsers.add_parser('remove')
    remove_parser.set_defaults(func=remove)
    remove_parser.add_argument('hostname', help='name of host to remove')
    remove_parser.add_argument('ip', help='ip of host to remove')

    shell_parser = subparsers.add_parser('shell')
    shell_parser.set_defaults(func=shell)

    args = parser.parse_args()

    logger.configure_onedns_logging(debug=args.debug)

    one_args = get_kwargs(args, 'one_')
    etcd_args = get_kwargs(args, 'etcd_')

    args.func(args, one_args, etcd_args)
