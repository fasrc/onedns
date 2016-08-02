import argparse

from onedns import utils
from onedns import server
from onedns import logger


def daemon(args, one_args):
    srv = server.OneDNS(args.domain, one_kwargs=one_args)
    srv.sync()
    srv.daemon(dns_port=args.dns_port)


def shell(args, one_args):
    srv = server.OneDNS(args.domain, one_kwargs=one_args)
    oneclient = srv._one
    ns = dict(one_dns=srv, oneclient=oneclient, log=logger.log)
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
        '--dns-port', required=False, default=5053, type=int,
        help="port for DNS server to listen on")

    shell_parser = subparsers.add_parser('shell')
    shell_parser.set_defaults(func=shell)

    args = parser.parse_args(args=args)

    logger.configure_onedns_logging(debug=args.debug)

    args_dict = vars(args)
    one_args = utils.get_kwargs_from_dict(args_dict, 'one_')

    args.func(args, one_args)
