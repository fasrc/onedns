import argparse

from onedns import monitor
from onedns import logger


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
    parser.add_argument('domain', help='DNS domain to use')
    args = parser.parse_args()
    logger.configure_onedns_logging(debug=args.debug)
    args_dict = vars(args)
    one_args = dict((i.replace('one_', ''), args_dict[i])
                    for i in args_dict.keys() if i.startswith('one_'))
    etcd_args = dict((i.replace('etcd_', ''), args_dict[i])
                     for i in args_dict.keys() if i.startswith('etcd_'))
    mon = monitor.OneMonitor(args.domain, one_kwargs=one_args,
                             etcd_kwargs=etcd_args)
    mon.run(args.interval)
