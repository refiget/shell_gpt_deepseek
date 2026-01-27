# ShellGPT DeepSeek

A fork of [shell-gpt](https://github.com/TheR1D/shell_gpt) with built-in support for **DeepSeek API** as the default model. This command-line productivity tool powered by AI large language models (LLM) offers streamlined generation of **shell commands, code snippets, documentation**, eliminating the need for external resources (like Google search).

Supports Linux, macOS, Windows and compatible with all major Shells like PowerShell, CMD, Bash, Zsh, etc.

## 主要特性

- **默认使用 DeepSeek API**：无需额外配置，开箱即用
- **支持多种 DeepSeek 模型**：`deepseek-chat`、`deepseek-coder` 等
- **完全兼容 OpenAI API 格式**：可无缝切换至其他 OpenAI 兼容的 API
- **保留原项目所有功能**：包括 Shell 命令生成、代码生成、聊天模式、REPL 模式等

## 安装方法

### 基础安装

```shell
pip install shell-gpt
```

### 从源码安装

```shell
# 克隆本仓库
git clone git@github.com:refiget/shell_gpt_deepseek.git
cd shell_gpt_deepseek

# 安装开发依赖
pip install -e .[dev]
```

### 环境变量配置

ShellGPT DeepSeek 默认使用 DeepSeek API 和 `deepseek-chat` 模型。你需要设置 `DEEPSEEK_API_KEY` 环境变量：

```shell
# 在 .bashrc 或 .zshrc 中添加
export DEEPSEEK_API_KEY=你的 DeepSeek API 密钥

# 或者在每次使用前临时设置
export DEEPSEEK_API_KEY=你的 DeepSeek API 密钥 && sgpt "你的提示"
```

你可以在 [DeepSeek 官方网站](https://www.deepseek.com/) 获取 API 密钥。

## 快速开始

### 基础问答

```shell
sgpt "什么是斐波那契数列"
# -> 斐波那契数列是一系列数字，其中每个数字都是前两个数字的和。
```

### 生成代码

```shell
sgpt --code "使用 Python 解决 FizzBuzz 问题"
```

```python
for i in range(1, 101):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
```

### 生成 Shell 命令

```shell
sgpt --shell "查找当前目录下所有 JSON 文件"
# -> find . -type f -name "*.json"
# -> [E]xecute, [D]escribe, [A]bort: e
```

### 聊天模式

```shell
sgpt --chat conversation_1 "请记住我的 favorite number: 4"
sgpt --chat conversation_1 "我的 favorite number + 4 是多少？"
# -> 你的 favorite number 是 4，所以 4 + 4 = 8。
```

### REPL 模式

```text
sgpt --repl temp
Entering REPL mode, press Ctrl+C to exit.
>>> 什么是 REPL？
REPL 代表读取-评估-打印循环（Read-Eval-Print Loop）。它是一种编程环境...
```

## 配置选项

你可以在运行时配置文件 `~/.config/shell_gpt/.sgptrc` 中设置以下参数：

```text
# API key, also it is possible to define DEEPSEEK_API_KEY env.
DEEPSEEK_API_KEY=your_api_key
# Base URL of the backend server.
DEEPSEEK_API_BASE_URL=https://api.deepseek.com/v1
# Max amount of cached message per chat session.
CHAT_CACHE_LENGTH=100
# Chat cache folder.
CHAT_CACHE_PATH=/tmp/shell_gpt/chat_cache
# Request cache length (amount).
CACHE_LENGTH=100
# Request cache folder.
CACHE_PATH=/tmp/shell_gpt/cache
# Request timeout in seconds.
REQUEST_TIMEOUT=60
# Default model to use.
DEFAULT_MODEL=deepseek-chat
# Default API to use.
DEFAULT_API=deepseek
# Default color for shell and code completions.
DEFAULT_COLOR=magenta
# When in --shell mode, default to "Y" for no input.
DEFAULT_EXECUTE_SHELL_CMD=false
# Disable streaming of responses
DISABLE_STREAMING=false
# The pygment theme to view markdown (default/describe role).
CODE_THEME=default
# Path to a directory with functions.
OPENAI_FUNCTIONS_PATH=/Users/user/.config/shell_gpt/functions
# Print output of functions when LLM uses them.
SHOW_FUNCTIONS_OUTPUT=false
# Allows LLM to use functions.
OPENAI_USE_FUNCTIONS=true
# Enforce LiteLLM usage (for local LLMs).
USE_LITELLM=false
```

## 完整参数列表

```text
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────╮
│   prompt      [PROMPT]  The prompt to generate completions for.                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --model            TEXT                       Large language model to use. [default: deepseek-chat]      │
│ --temperature      FLOAT RANGE [0.0<=x<=2.0]  Randomness of generated output. [default: 0.0]             │
│ --top-p            FLOAT RANGE [0.0<=x<=1.0]  Limits highest probable tokens (words). [default: 1.0]     │
│ --md             --no-md                      Prettify markdown output. [default: md]                    │
│ --editor                                      Open $EDITOR to provide a prompt. [default: no-editor]     │
│ --cache                                       Cache completion results. [default: cache]                 │
│ --version                                     Show version.                                              │
│ --help                                        Show this message and exit.                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Assistance Options ─────────────────────────────────────────────────────────────────────────────────────╮
│ --shell           -s                      Generate and execute shell commands.                           │
│ --interaction         --no-interaction    Interactive mode for --shell option. [default: interaction]    │
│ --describe-shell  -d                      Describe a shell command.                                      │
│ --code            -c                      Generate only code.                                            │
│ --functions           --no-functions      Allow function calls. [default: functions]                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Chat Options ───────────────────────────────────────────────────────────────────────────────────────────╮
│ --chat                 TEXT  Follow conversation with id, use "temp" for quick session. [default: None]  │
│ --repl                 TEXT  Start a REPL (Read–eval–print loop) session. [default: None]                │
│ --show-chat            TEXT  Show all messages from provided chat id. [default: None]                    │
│ --list-chats  -lc            List all existing chat ids.                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Role Options ───────────────────────────────────────────────────────────────────────────────────────────╮
│ --role                  TEXT  System role for GPT model. [default: None]                                 │
│ --create-role           TEXT  Create role. [default: None]                                               │
│ --show-role             TEXT  Show role. [default: None]                                                 │
│ --list-roles   -lr            List roles.                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Docker 使用

使用 `DEEPSEEK_API_KEY` 环境变量和 docker 卷来存储缓存运行容器：

```shell
docker run --rm \
           --env DEEPSEEK_API_KEY=api_key \
           --env OS_NAME=$(uname -s) \
           --env SHELL_NAME=$(echo $SHELL) \
           --volume gpt-cache:/tmp/shell_gpt \
       ghcr.io/ther1d/shell_gpt -s "update my system"
```

## 与原项目的区别

1. **默认 API 切换**：默认使用 DeepSeek API 而非 OpenAI API
2. **默认模型更新**：默认使用 `deepseek-chat` 模型
3. **新增配置项**：添加了 `DEEPSEEK_API_KEY` 和 `DEEPSEEK_API_BASE_URL` 配置
4. **自动模型选择**：当使用 DeepSeek API 时，自动选择合适的 DeepSeek 模型

## 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 许可证

本项目基于 MIT 许可证，详情请参阅 [LICENSE](LICENSE) 文件。

## 致谢

- 感谢 [TheR1D](https://github.com/TheR1D) 创建的原始 [shell-gpt](https://github.com/TheR1D/shell_gpt) 项目
- 感谢 [DeepSeek](https://www.deepseek.com/) 提供的高性能语言模型
