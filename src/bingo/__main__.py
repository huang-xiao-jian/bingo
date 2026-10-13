"""程序入口：`uv run python -m bingo [名字]`。"""

import argparse
import sys

from bingo import __version__, hello


def main(argv: list[str] | None = None) -> int:
    """解析命令行参数并打印问候语，返回进程退出码。"""
    parser = argparse.ArgumentParser(prog="bingo", description="Hello World 示例")
    parser.add_argument("name", nargs="?", default="world", help="要问候的名字")
    parser.add_argument("--version", action="version", version=f"bingo {__version__}")
    args = parser.parse_args(argv)

    print(hello(args.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
