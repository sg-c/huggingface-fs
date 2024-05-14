import argparse
import sys

from model import ModelManager
from peer import PeerManager, PeerStore


peer_store = PeerStore()
peer_manager = PeerManager(peer_store)

model_manager = ModelManager()


def print_usage():
    print("Usage: python hffs.py cmd [subcmd] [opts]")
    sys.exit(1)


def peer_cmd(args):
    if args.peer_command == "add":
        peer_manager.add_peer(args.IP, args.port)
    elif args.peer_command == "rm":
        peer_manager.remove_peer(args.IP, args.port)
    elif args.peer_command == "ls":
        peer_manager.list_peers()
    else:  # no matching subcmd
        raise ValueError("Invalid subcommand")


def model_cmd(arg):
    if args.model_command == "add":
        model_manager.add_model(args.repo_id, args.branch, args.revision)


def exec_cmd(args):
    if args.command == "peer":
        peer_cmd(args)
    elif args.command == "model":
        model_cmd(args)
    elif args.command == "start":
        pass
    elif args.command == "stop":
        pass
    else:
        raise ValueError("Invalid subcommand")


def arg_parser():
    parser = argparse.ArgumentParser(prog='hffs')
    subparsers = parser.add_subparsers(dest='command')

    # hffs start
    start_parser = subparsers.add_parser('start')

    # hffs stop [--destroy-cache]
    stop_parser = subparsers.add_parser('stop')
    stop_parser.add_argument('--destroy-cache', action='store_true')

    # hffs peer {add,rm,ls} IP [--port port]
    peer_parser = subparsers.add_parser('peer')
    peer_subparsers = peer_parser.add_subparsers(dest='peer_command')
    peer_add_parser = peer_subparsers.add_parser('add')
    peer_add_parser.add_argument('IP')
    peer_add_parser.add_argument('--port', type=int)
    peer_rm_parser = peer_subparsers.add_parser('rm')
    peer_rm_parser.add_argument('IP')
    peer_rm_parser.add_argument('--port', type=int)
    peer_ls_parser = peer_subparsers.add_parser('ls')

    # hffs model {ls,add,rm} [--repo-id id] [--branch BRANCH] [--revision REVISION]
    model_parser = subparsers.add_parser('model')
    model_subparsers = model_parser.add_subparsers(dest='model_command')
    model_ls_parser = model_subparsers.add_parser('ls')
    model_ls_parser.add_argument('--repo_id')
    model_add_parser = model_subparsers.add_parser('add')
    model_add_parser.add_argument('repo_id')
    model_add_parser.add_argument('--branch')
    model_add_parser.add_argument('--revision')
    model_rm_parser = model_subparsers.add_parser('rm')
    model_rm_parser.add_argument('repo_id')
    model_rm_parser.add_argument('--branch')
    model_rm_parser.add_argument('--revision')

    return parser.parse_args()


if __name__ == "__main__":
    args = arg_parser()
    try:
        exec_cmd(args)
    finally:
        peer_store.close()
