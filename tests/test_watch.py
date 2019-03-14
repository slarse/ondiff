import asyncio

import pytest
from asynctest import CoroutineMock

from ondiff import watch


@pytest.fixture
def files(tmp_path):
    filepaths = [tmp_path / f"file{i}" for i in range(5)]
    for path in filepaths:
        path.touch()
    yield filepaths


@pytest.fixture
def execute_mock(mocker):
    yield mocker.patch("ondiff.watch.execute", new=CoroutineMock())


@pytest.fixture
def subproc_mock_factory(mocker):
    def _subproc_mock(stdout=b"Stdout stuff", stderr=b"", return_code=0):
        proc_mock = CoroutineMock()
        proc_mock.return_value = 0

        async def communicate():
            return stdout, stderr

        proc_mock.communicate = communicate
        create_subprocess_exec_mock = CoroutineMock(
            spec=asyncio.create_subprocess_exec, return_value=proc_mock
        )
        return mocker.patch(
            "asyncio.create_subprocess_exec", new=create_subprocess_exec_mock
        )

    yield _subproc_mock


@pytest.mark.asyncio
class TestWatchFiles:
    """Tests for the watch_files function."""

    @pytest.mark.parametrize("return_code", (0, 1))
    async def test_command_executed_when_file_changes(
        self, files, event_loop, subproc_mock_factory, return_code
    ):
        """Test the happy path."""
        subproc_mock = subproc_mock_factory(return_code=return_code)
        cmd = "echo 'hello world'".split()
        wait_time = 0.1
        change_file = files[len(files) // 2]
        shutdown_event = asyncio.Event(loop=event_loop)
        task = watch.watch_files(
            files, cmd, shutdown_event, wait_time=wait_time
        )
        event_loop.create_task(task)

        # yield control to watcher for initial hash calcs
        await asyncio.sleep(wait_time)
        change_file.write_text("hello")
        await asyncio.sleep(wait_time * 2)

        # finish up
        shutdown_event.set()
        await asyncio.sleep(wait_time * 2)

        # file changes should now have been detected
        subproc_mock.assert_called_once_with(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            shell=False,
        )
