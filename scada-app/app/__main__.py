import argparse

from . import __version__, run_icmp, run_mbus

# parse args
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='cmd', required=True)
# version subparser
parser_version = subparsers.add_parser('version', help='show app version')
# icmp subparser
parser_icmp = subparsers.add_parser('icmp', help='start icmp job')
parser_icmp.add_argument('-d', '--debug', action='store_true', help='set debug mode')
# mbus parser
parser_mbus = subparsers.add_parser('mbus', help='start mbus job')
parser_mbus.add_argument('-d', '--debug', action='store_true', help='set debug mode')
# mbus-export parser
parser_mbus_export = subparsers.add_parser('mbus-export', help='start mbus-export job')
parser_mbus_export.add_argument('-d', '--debug', action='store_true', help='set debug mode')
# parse
args = parser.parse_args()

# run selected command
if args.cmd == 'version':
    print(__version__)
elif args.cmd == 'icmp':
    run_icmp(debug=args.debug)
elif args.cmd == 'mbus':
    run_mbus(debug=args.debug)
elif args.cmd == 'mbus-export':
    run_mbus_export(debug=args.debug)
