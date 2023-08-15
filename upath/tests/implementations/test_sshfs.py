import tempfile
from pathlib import Path

import mockssh
import pytest

from upath import UPath
from upath.implementations.sshfs import SSHPath

from ..cases import BaseTests

STATIC = (Path(__file__).parent.parent / "static").resolve()
USERS = {"user": STATIC / "user.key"}


class TestSSHPath(BaseTests):
    @pytest.fixture(autouse=True)
    def path(self, local_testdir):
        """Start a mock SSH server."""
        with mockssh.Server(USERS) as server, tempfile.TemporaryDirectory() as path:
            self.path = UPath(
                f"ssh://user@{server.host}:{server.port}/{path}",
                client_keys=[USERS["user"]],
            )
            self.prepare_file_system()
            yield

    def test_is_SSHPath(self):
        assert isinstance(self.path, SSHPath)
