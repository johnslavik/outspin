"""CLI for inspecting keypresses."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

if sys.platform == "win32" or sys.platform == "cygwin":
    from outspin.windows import _MODS, _getch

    EXIT_CODE = 0xC000013A
else:
    from signal import SIGINT

    from outspin.unix import _MODS, _getch

    EXIT_CODE = SIGINT + 128


def main(getch: Callable[[], str] = _getch) -> None:
    """Read keypresses and display their raw and translated forms."""
    print("press keys to inspect (Ctrl+C twice to quit)", file=sys.stderr)
    prev = ""
    while True:
        raw = getch()
        key = _MODS.get(raw, raw)
        print(f"{key!r:16s} raw: {raw!r}")
        if key == prev == "^C":
            print("good bye!", file=sys.stderr)
            raise SystemExit(EXIT_CODE)
        prev = key


if __name__ == "__main__":
    main()
