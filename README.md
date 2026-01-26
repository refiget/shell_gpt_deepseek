# ShellGPT - DeepSeek Edition

> 基于 [TheR1D/shell_gpt](https://github.com/TheR1D/shell_gpt) 的 Fork 版本，添加了 DeepSeek API 支持

ShellGPT 是一个由 AI 大语言模型（LLM）驱动的命令行生产力工具。该命令行工具提供了**Shell 命令、代码片段、文档**的生成，无需外部资源（如 Google 搜索）。支持 Linux、macOS、Windows，并与所有主要 Shell（如 PowerShell、CMD、Bash、Zsh 等）兼容。

## 🚀 主要改动

本项目在原版 ShellGPT 的基础上，添加了以下功能：

- ✅ **DeepSeek API 支持**：完全兼容 DeepSeek API，支持 `deepseek-chat` 和 `deepseek-coder` 模型
- ✅ **环境变量配置**：支持通过环境变量 `DEEPSEEK_API_KEY` 配置 API 密钥
- ✅ **快捷参数**：新增 `--deepseek` 参数，快速切换到 DeepSeek 模型
- ✅ **向后兼容**：保留原版所有功能，不影响 OpenAI/Anthropic 等模型的使用

## 📦 安装

### 使用 pipx 安装（推荐）

```bash
pipx install shell-gpt
```

### 使用 pip 安装

```bash
pip install shell-gpt
```

## 🔑 配置 DeepSeek API

### 方法 1：使用环境变量（推荐）

```bash
export DEEPSEEK_API_KEY="your_deepseek_api_key_here"
```

为了永久生效，可以将上述命令添加到你的 shell 配置文件中：

- **Bash**: `~/.bashrc` 或 `~/.bash_profile`
- **Zsh**: `~/.zshrc`

### 方法 2：使用配置文件

在 `~/.config/shell_gpt/.sgptrc` 文件中添加：

```text
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_API_BASE_URL=https://api.deepseek.com/v1
```

## 📖 使用方法

### 基础对话

```bash
# 使用 DeepSeek 模型
sgpt --model deepseek-chat "你好"

# 使用快捷参数
sgpt --deepseek "解释什么是量子计算"
```

### 生成 Shell 命令

```bash
# 生成并执行 shell 命令
sgpt --model deepseek-chat --shell "查看端口占用"

# 使用快捷参数
sgpt --deepseek --shell "查找所有 .json 文件"
```

### 生成代码

```bash
# 生成代码片段
sgpt --model deepseek-chat --code "快速排序算法"

# 使用快捷参数
sgpt --deepseek --code "Python 实现斐波那契数列"
```

### 聊天模式

```bash
# 开始一个对话会话
sgpt --model deepseek-chat --chat my_chat "请记住我的名字是张三"

# 继续对话
sgpt --model deepseek-chat --chat my_chat "我的名字是什么？"
```

### REPL 模式

```bash
# 进入交互式 REPL 模式
sgpt --model deepseek-chat --repl temp

# 使用快捷参数
sgpt --deepseek --repl temp
```

## 🎯 支持的 DeepSeek 模型

- `deepseek-chat`：对话模型，适用于通用对话和问答
- `deepseek-coder`：代码模型，专门用于代码生成和编程任务

## 🔧 配置文件

ShellGPT 的配置文件位于 `~/.config/shell_gpt/.sgptrc`，支持的配置项：

```text
# DeepSeek API 密钥
DEEPSEEK_API_KEY=your_api_key_here

# DeepSeek API 基础 URL（默认为 https://api.deepseek.com/v1）
DEEPSEEK_API_BASE_URL=https://api.deepseek.com/v1

# OpenAI API 密钥（如果需要使用 OpenAI 模型）
OPENAI_API_KEY=your_openai_api_key_here

# 默认模型
DEFAULT_MODEL=deepseek-chat

# 请求超时时间（秒）
REQUEST_TIMEOUT=60

# 其他配置项...
```

## 🌟 原版功能

本项目保留了原版 ShellGPT 的所有功能，包括：

- ✅ Shell 命令生成与执行
- ✅ 代码生成
- ✅ 聊天模式
- ✅ REPL 模式
- ✅ 自定义角色（Roles）
- ✅ 函数调用（Function Calling）
- ✅ Shell 集成
- ✅ 请求缓存
- ✅ Markdown 渲染

## 📚 更多功能

关于 ShellGPT 的更多功能和详细使用方法，请参考 [原版文档](https://github.com/TheR1D/shell_gpt)。

## 🔗 相关链接

- [原版 ShellGPT](https://github.com/TheR1D/shell_gpt)
- [DeepSeek API 文档](https://platform.deepseek.com/api-docs/)
- [获取 DeepSeek API Key](https://platform.deepseek.com/api_keys)

## 📝 注意事项

1. **API 密钥安全**：请勿将 API 密钥提交到版本控制系统
2. **费用说明**：DeepSeek API 按使用量计费，请参考 [DeepSeek 定价](https://platform.deepseek.com/pricing)
3. **模型选择**：根据任务类型选择合适的模型，`deepseek-chat` 适合通用对话，`deepseek-coder` 适合编程任务

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目遵循原版 ShellGPT 的 [MIT 许可证](LICENSE)。

---

**注意**：本项目是基于 [TheR1D/shell_gpt](https://github.com/TheR1D/shell_gpt) 的 Fork 版本，主要用于添加 DeepSeek API 支持。如需使用原版功能或获取最新更新，请访问原版仓库。
