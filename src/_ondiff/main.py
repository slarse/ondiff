"""Main module for ondiff.

.. module:: main
    :synopsis: Main module for ondiff.

.. moduleauthor:: Simon Larsén
"""

import argparse
import asyncio
import pathlib
import sys
from typing import List

import _ondiff.watch


def main():
    args = _parse_args(sys.argv[1:])

    loop = asyncio.get_event_loop()
    shutdown_signal = asyncio.Event(loop=loop)
    task = _ondiff.watch.watch_files(args.files, args.command, shutdown_signal)

    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        print("Received keyboard interrupt, exiting ...")
        shutdown_signal.set()
    finally:
        loop.close()


def _parse_args(sys_args: List[str]) -> argparse.Namespace:
    parser = _create_parser()
    args = parser.parse_args(sys_args)

    if not args.path.exists():
        print(f"{args.path}: No such file or directory", file=sys.stderr)

    files = [args.path] if args.path.is_file() else list(args.path.rglob("*"))

    args_dict = vars(args)
    del args_dict["path"]
    args_dict["command"] = args.command.split(" ")
    args_dict["files"] = files

    return argparse.Namespace(**args_dict)


def _create_parser() -> argparse.ArgumentParser:
    """Create the CLI parser."""
    parser = argparse.ArgumentParser(prog="ondiff")

    parser.add_argument(
        "path", type=pathlib.Path, help="Path to a file or directory to watch."
    )
    parser.add_argument(
        "-c", "--command", type=str, help="Command to run upon change.", required=True,
    )

    return parser
