"""Functions for watching files and directories, and acting on changes.

.. module:: watch
    :synopsis: Functions for watching files and directories, and acting on
        changes.

.. moduleauthor:: Simon Larsén
"""


import sys
from pathlib import Path
from typing import List
from dataclasses import dataclass, field
import asyncio

import logging

from hashlib import md5

LOGGER = logging.getLogger(name=__file__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


@dataclass(frozen=True, eq=True)
class HashedFile:
    """Holds the path to a file, and its hash."""

    path: Path
    checksum: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(
            self, "checksum", md5(self.path.read_bytes()).hexdigest()
        )


async def watch_files(
    files: List[Path],
    cmd: List[str],
    shutdown: asyncio.Event,
    wait_time: int = 1,
):
    """Watch files for changes indefinitely.

    Args:
        files: A list of files to watch.
        cmd: A command to run when a file changes.
        shutdown: An event that can signal this coroutine to terminate.
        wait_time: The amount of time (in seconds) to wait between each scan of
            the watched files.
    Returns:
        A c
        """
    files = [file for file in files if file.is_file()]
    LOGGER.info("watching files %s", [str(p) for p in files])
    hashes = set(HashedFile(path) for path in files)

    loop = asyncio.get_event_loop()

    while not shutdown.is_set():
        await asyncio.sleep(wait_time)
        new_hashes = set(HashedFile(path) for path in files)
        diff = hashes - new_hashes
        if diff:
            for hf in diff:
                LOGGER.info("%s changed", hf.path.name)
                loop.create_task(execute(cmd, hf.path))
            hashes = new_hashes


async def execute(cmd, file):
    LOGGER.info("Executing '%s' on '%s'", " ".join(cmd), file)
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        shell=False,
    )

    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        LOGGER.error("non-zero exit status from %s", " ".join(cmd))
    if stdout:
        LOGGER.info(
            "stdout: %s", stdout.decode(encoding=sys.getdefaultencoding())
        )
    if stderr:
        LOGGER.info(
            "stderr: %s", stderr.decode(encoding=sys.getdefaultencoding())
        )
