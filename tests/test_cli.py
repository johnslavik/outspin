from __future__ import annotations

import os
import shutil
from unittest.mock import Mock

import pytest

from outspin.__main__ import main


@pytest.mark.skipif(
    not os.getenv("CI"),
    reason="Console script availability is tested in CI",
)
def test_console_script_installed() -> None:
    """Test that the CLI can be imported and run."""
    assert shutil.which("outspin") is not None


def test_banner(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        main(getch=Mock(side_effect="\x03\x03"))
    assert "Ctrl+C twice to quit" in capsys.readouterr().err


def test_basic(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        main(getch=Mock(side_effect="\x03abc\x03\x03"))
    lines = capsys.readouterr().out.strip().splitlines()
    assert "'^C'" in lines[0]
    assert "'a'" in lines[1]
    assert "'b'" in lines[2]
    assert "'c'" in lines[3]
    assert "'^C'" in lines[4]
    assert "'^C'" in lines[5]
    assert len(lines) == 6
