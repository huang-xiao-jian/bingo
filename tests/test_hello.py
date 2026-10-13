"""pytest 最小示例：直接 assert，失败时自动展开左右两边的值。"""

import sys

from bingo import hello
from bingo.__main__ import main


def test_hello_default() -> None:
    assert hello() == "Hello, world!"


def test_hello_with_name() -> None:
    assert hello("jerry") == "Hello, jerry!"


def test_main_prints_and_exits_zero(capsys) -> None:
    assert main(["jerry"]) == 0
    assert capsys.readouterr().out == "Hello, jerry!\n"


def test_main_reads_argv(monkeypatch) -> None:
    monkeypatch.setattr(sys, "argv", ["bingo"])
    assert main() == 0
