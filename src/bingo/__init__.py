"""bingo 包入口。"""

__all__ = ["hello"]
__version__ = "0.1.0"


def hello(name: str = "world") -> str:
    """返回一句问候。"""
    return f"Hello, {name}!"
