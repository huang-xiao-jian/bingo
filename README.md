# bingo —— Python 学习项目（现代工具链版）

一个为「从 Node.js 迁移过来的新人」准备的 Python 学习项目。
工具链对标你在 JS 生态里的肌肉记忆：**uv ≈ npm，Ruff ≈ ESLint + Prettier，pyright ≈ tsc --noEmit，pytest ≈ Jest**。

## 1. 三十秒了解这套工具

| 你要做的事     | Node.js              | 本项目（Python）                   |
| -------------- | -------------------- | ---------------------------------- |
| 装依赖         | `npm i pkg`          | `uv add pkg`                       |
| 装开发依赖     | `npm i -D pkg`       | `uv add --dev pkg`                 |
| 锁文件         | `package-lock.json`  | `uv.lock`（**务必提交**）          |
| 干净还原环境   | `npm ci`             | `uv sync --locked`                 |
| 跑脚本         | `node src/index.js`  | `uv run python -m bingo`           |
| 格式化         | `prettier --write .` | `uv run ruff format .`             |
| Lint           | `eslint . --fix`     | `uv run ruff check . --fix`        |
| 类型检查       | `tsc --noEmit`       | `uv run pyright`                   |
| 测试           | `jest` / `vitest`    | `uv run pytest`                    |
| 测试覆盖率     | `jest --coverage`    | `uv run pytest --cov`              |
| 切换解释器版本 | nvm                  | `uv python install 3.13`（已内置） |

关键心法：**只要在项目目录里，所有 Python 命令前面加 `uv run`**。
它会自动创建/激活虚拟环境，你永远不需要手动 `source .venv/bin/activate`，
也不会发生 Node 开发者最容易踩的坑——`pip install` 把包装进全局环境。

## 2. 目录结构

```text
bingo/
├── pyproject.toml        # 单一事实来源 ≈ package.json + 各工具配置合并
├── uv.lock               # 精确版本+哈希锁文件 ≈ package-lock.json（要提交）
├── .python-version       # 锁定 Python 3.13 ≈ .nvmrc
├── .venv/                # 项目级虚拟环境 ≈ node_modules（不提交）
├── src/bingo/            # 你的包（src-layout，见下文"为什么"）
│   ├── __init__.py       # ≈ index.js：hello() 在这里定义并导出
│   └── __main__.py       # 入口：`python -m bingo` 执行的正是它
├── tests/                # pytest 测试，对照 Jest 的 __tests__
│   └── test_hello.py     # 最小测试：assert 直断 + capsys + monkeypatch
├── .github/workflows/ci.yml  # 流水线：format → lint → typecheck → test
└── .vscode/settings.json     # 装了 Ruff 扩展后保存即自动格式化
```

### 为什么代码放 `src/` 下面？

Node 里 `require()` 会逐级向上找 `node_modules`，所以脚本随便放哪都能跑。
Python 的 `import` 只查一个扁平的 `sys.path`，把源码直接摊在根目录时，
「你写的包」和「第三方包」在 import 系统眼里没有区别，容易互相遮蔽。
`src/` 布局强制你只能通过「已安装的包」来 import 自己，问题会在写代码时暴露而不是上线后。
这是 2024 年后 Python 社区的公认最佳实践。

## 3. 第一天上手清单

```bash
# 0. 前置：装好 uv（一次性）
#    macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh
#    大陆网络受限时可用镜像：brew install uv，或从 GitHub Release 手动下载

# 1. clone 或进入项目后，一条命令还原全部环境（含 Python 版本）
uv sync

# 2. 跑示例程序
uv run python -m bingo 你的名字
uv run python -m bingo --version

# 3. 跑质量套件（和 CI 完全一致）
uv run ruff format .         # 格式化
uv run ruff check . --fix    # lint + 自动修复
uv run pyright               # 类型检查
uv run pytest --cov          # 测试 + 覆盖率

# 4. 学完示例后，加你自己的第一个依赖
uv add requests
```

## 4. 依赖源说明（大陆网络）

官方 PyPI 源在中国大陆访问不稳定。本项目已在 `pyproject.toml` 的
`[[tool.uv.index]]` 中固定使用阿里云镜像，并写进 `uv.lock`——
**任何人 clone 后 `uv sync` 即可，无需额外配置**。想换清华源，改那一行 `url` 后重新 `uv lock` 即可。
CI（GitHub Actions）在海外 runner 上运行时同样走镜像；若你自建 CI 在境外且希望走官方源，删掉该 index 段即可。

> 注意：uv 下载 **Python 解释器本身** 走的是 GitHub Releases，与 PyPI 镜像无关；
> 若首次 `uv sync` 拉解释器慢，可先手动 `uv python install 3.13`。

## 5. 给 Node 开发者的五个心智转换

1. **全局 vs 项目级**：`npm i` 默认项目级，`pip i` 默认全局。所以永远 `uv run` 或 `uv add`，别裸用 `pip`。
2. **没有嵌套兜底**：依赖冲突时 npm 会静默装两份，Python 直接报错。报错不是坏事——uv 的错误信息会指出冲突链，按提示升降级即可。
3. **版本范围写法**：`^1.2.3`、`~1.2.3` 在 uv 里可用且语义≈npm（PEP 440 原生写法是 `>=1.2.3, <2.0.0`）。
4. **类型系统是可选的**：pyright 不做编译，只做检查（像 `tsc --noEmit`）。建议保持 `standard` 模式起步，别一上来开 `strict` 劝退自己。
5. **`await` 更严格**：JS 里 Promise 不 await 也只是悬着；Python 里协程不 await 拿到的是 coroutine 对象，什么都不会发生。忘了写 `asyncio.run()` 或 `await` 是新人第一大坑。

## 6. 学习路线建议

当前源码刻意保持 Hello World 级别：一个 `hello()` 函数、一个能 `python -m bingo` 运行的入口、一组最小测试。

- 读 `src/bingo/__init__.py` 和 `__main__.py`：熟悉 f-string、类型注解、argparse、`if __name__ == "__main__"` 这些最小要素。
- 读 `tests/test_hello.py`：感受 pytest 直接用 `assert`，以及 `capsys`（捕获 stdout）、`monkeypatch`（改全局状态）两个最常用的 fixture，≈ Jest 的 mock/spy。
- 改代码 → 保存（VS Code 自动格式化）→ `uv run pytest`，体验一次完整内循环。
- 需要新功能时，用 `uv add` 加依赖（如 `fastapi uvicorn` 对照 Express），并在 `src/bingo/` 下新增模块即可，工具链不用动。
