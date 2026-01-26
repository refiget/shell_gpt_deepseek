# GitHub Fork 项目与项目规范教程

本教程将指导你如何正确地 Fork 一个 GitHub 项目，以及如何规范地组织和管理你的项目。

## 目录

1. [什么是 Fork](#什么是-fork)
2. [如何 Fork 一个项目](#如何-fork-一个项目)
3. [如何克隆和管理 Fork 的项目](#如何克隆和管理-fork-的项目)
4. [如何向原项目贡献代码](#如何向原项目贡献代码)
5. [项目结构规范](#项目结构规范)
6. [文档编写规范](#文档编写规范)
7. [最佳实践](#最佳实践)

---

## 什么是 Fork

**Fork** 是 GitHub 上的一个功能，允许你将别人的仓库复制到自己的 GitHub 账户下。Fork 后的仓库是一个独立的副本，你可以自由地修改它，而不会影响原项目。

### Fork 的主要用途：

1. **贡献代码**：修改开源项目并提交 Pull Request
2. **自定义开发**：基于现有项目进行定制开发
3. **学习研究**：研究优秀项目的代码结构和实现
4. **备份保存**：保存你喜欢的项目到自己的账户

---

## 如何 Fork 一个项目

### 步骤 1：访问目标项目

在浏览器中打开你想要 Fork 的项目页面，例如：
```
https://github.com/TheR1D/shell_gpt
```

### 步骤 2：点击 Fork 按钮

在项目页面的右上角，点击 **"Fork"** 按钮。

### 步骤 3：配置 Fork 选项

GitHub 会弹出一个对话框，让你配置 Fork 的选项：

- **Owner**：选择 Fork 到哪个账户（个人账户或组织）
- **Repository name**：仓库名称（默认与原项目相同）
- **Description**：仓库描述（可选）
- **Copy the main branch only**：是否只复制主分支（推荐勾选）

点击 **"Create fork"** 完成创建。

### 步骤 4：确认 Fork 成功

Fork 成功后，GitHub 会自动跳转到你的新仓库页面，URL 类似：
```
https://github.com/your-username/shell_gpt
```

---

## 如何克隆和管理 Fork 的项目

### 步骤 1：克隆 Fork 的仓库到本地

```bash
# 克隆你的 Fork 仓库
git clone https://github.com/your-username/shell_gpt.git
cd shell_gpt
```

### 步骤 2：添加原仓库为远程源（Upstream）

为了保持与原项目同步，需要添加原仓库为远程源：

```bash
# 添加原仓库为 upstream 远程源
git remote add upstream https://github.com/TheR1D/shell_gpt.git

# 验证远程源配置
git remote -v
```

输出应该类似：
```
origin    https://github.com/your-username/shell_gpt.git (fetch)
origin    https://github.com/your-username/shell_gpt.git (push)
upstream  https://github.com/TheR1D/shell_gpt.git (fetch)
upstream  https://github.com/TheR1D/shell_gpt.git (push)
```

### 步骤 3：保持 Fork 与原项目同步

定期从原项目拉取最新更改：

```bash
# 切换到主分支
git checkout main

# 从 upstream 拉取最新更改
git fetch upstream

# 合并 upstream 的主分支到你的本地主分支
git merge upstream/main

# 推送更新到你的 Fork
git push origin main
```

### 步骤 4：创建功能分支

在进行修改时，总是创建新的分支：

```bash
# 创建并切换到新分支
git checkout -b feature/deepseek-api-support

# 或者
git checkout -b fix/bug-description
```

### 步骤 5：提交更改

```bash
# 查看修改的文件
git status

# 添加修改的文件
git add .

# 提交更改（使用规范的提交信息）
git commit -m "feat: 添加 DeepSeek API 支持"
```

### 步骤 6：推送到你的 Fork

```bash
# 推送当前分支到你的 Fork
git push origin feature/deepseek-api-support
```

---

## 如何向原项目贡献代码

### 步骤 1：创建 Pull Request

1. 访问你的 Fork 仓库页面
2. 点击 **"Compare & pull request"** 按钮
3. 确保选择正确的分支：
   - **base repository**: 原项目（TheR1D/shell_gpt）
   - **base**: main（或原项目指定的目标分支）
   - **head repository**: 你的 Fork（your-username/shell_gpt）
   - **compare**: 你的功能分支（feature/deepseek-api-support）

### 步骤 2：填写 Pull Request 信息

**标题**：简洁明了地描述更改
```
feat: 添加 DeepSeek API 支持
```

**描述**：详细说明更改内容、原因和测试情况

```markdown
## 更改说明
- 添加了 DeepSeek API 支持
- 支持环境变量配置 API 密钥
- 新增 `--deepseek` 快捷参数

## 测试情况
- ✅ 基础对话测试通过
- ✅ Shell 命令生成测试通过
- ✅ 代码生成测试通过

## 相关 Issue
Closes #123
```

### 步骤 3：提交 Pull Request

点击 **"Create pull request"** 提交。

### 步骤 4：响应反馈

维护者可能会提出修改建议，你需要：
1. 在本地进行修改
2. 提交并推送到你的分支
3. Pull Request 会自动更新

---

## 项目结构规范

### 标准项目结构

```
project-name/
├── .github/                  # GitHub 特定文件
│   ├── workflows/            # GitHub Actions 工作流
│   ├── ISSUE_TEMPLATE/       # Issue 模板
│   └── PULL_REQUEST_TEMPLATE.md  # PR 模板
├── docs/                     # 项目文档
│   ├── api.md               # API 文档
│   ├── contributing.md       # 贡献指南
│   └── tutorial.md          # 教程文档
├── src/                      # 源代码
│   ├── module1/             # 模块 1
│   ├── module2/             # 模块 2
│   └── __init__.py
├── tests/                    # 测试代码
│   ├── unit/                # 单元测试
│   ├── integration/         # 集成测试
│   └── conftest.py          # pytest 配置
├── scripts/                  # 脚本文件
│   ├── build.sh             # 构建脚本
│   └── deploy.sh            # 部署脚本
├── examples/                 # 示例代码
├── .gitignore               # Git 忽略文件
├── .env.example             # 环境变量示例
├── LICENSE                  # 许可证
├── README.md                # 项目说明
├── CHANGELOG.md             # 变更日志
├── pyproject.toml           # Python 项目配置
└── requirements.txt         # Python 依赖
```

### 文件命名规范

- **Python 文件**：使用小写字母和下划线，如 `config.py`, `api_handler.py`
- **测试文件**：以 `test_` 开头，如 `test_config.py`, `test_api.py`
- **文档文件**：使用小写字母和连字符，如 `api-guide.md`, `getting-started.md`
- **目录名**：使用小写字母和下划线，如 `api_handlers/`, `utils/`

### 代码组织原则

1. **单一职责**：每个模块/类只负责一个功能
2. **高内聚低耦合**：相关功能放在一起，模块间依赖最小化
3. **清晰的层次结构**：按功能或层次组织代码
4. **易于测试**：代码结构便于编写测试

---

## 文档编写规范

### README.md 规范

README.md 是项目的门面，应该包含以下内容：

```markdown
# 项目名称

> 一句话描述项目的核心价值

简短的项目描述（2-3句话）。

## ✨ 特性

- 特性 1：描述
- 特性 2：描述
- 特性 3：描述

## 📦 安装

### 前置要求

- Python 3.8+
- Node.js 16+

### 安装步骤

```bash
pip install project-name
```

## 🚀 快速开始

```python
import project_name

# 使用示例
result = project_name.do_something()
print(result)
```

## 📖 使用方法

### 基础用法

详细说明...

### 高级用法

详细说明...

## 🔧 配置

说明配置选项...

## 🧪 测试

```bash
pytest
```

## 🤝 贡献

欢迎贡献！请阅读 [贡献指南](CONTRIBUTING.md)。

## 📄 许可证

MIT License

## 🔗 相关链接

- [项目主页](https://github.com/username/project)
- [文档](https://docs.example.com)
- [问题反馈](https://github.com/username/project/issues)
```

### CONTRIBUTING.md 规范

```markdown
# 贡献指南

感谢你考虑为项目做出贡献！

## 如何贡献

### 报告问题

1. 检查是否已存在相同 Issue
2. 使用 Issue 模板创建新 Issue
3. 提供详细的复现步骤

### 提交代码

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 代码规范

### Python 代码规范

- 遵循 PEP 8 规范
- 使用类型注解
- 编写单元测试

### 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型（type）：
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

示例：
```
feat(api): 添加 DeepSeek API 支持

- 添加了 API 客户端
- 支持环境变量配置
- 新增单元测试

Closes #123
```
```

### CHANGELOG.md 规范

```markdown
# 更新日志

所有重要的项目更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.2.0] - 2024-01-15

### 新增
- 添加 DeepSeek API 支持
- 新增 `--deepseek` 快捷参数
- 支持环境变量配置

### 修复
- 修复 API 密钥读取问题
- 修复缓存机制的 bug

### 变更
- 重构配置模块
- 更新依赖版本

## [1.1.0] - 2024-01-01

### 新增
- 添加聊天模式
- 添加 REPL 模式

## [1.0.0] - 2023-12-15

### 新增
- 首次发布
```

---

## 最佳实践

### 1. Git 工作流

#### 功能开发流程

```bash
# 1. 确保主分支是最新的
git checkout main
git pull upstream main

# 2. 创建功能分支
git checkout -b feature/your-feature-name

# 3. 进行开发
# ... 编写代码 ...

# 4. 提交更改
git add .
git commit -m "feat: 添加新功能"

# 5. 推送到远程
git push origin feature/your-feature-name

# 6. 创建 Pull Request
```

#### Bug 修复流程

```bash
# 1. 创建修复分支
git checkout -b fix/bug-description

# 2. 修复 bug
# ... 修复代码 ...

# 3. 提交更改
git add .
git commit -m "fix: 修复 xxx 的问题"

# 4. 推送并创建 PR
git push origin fix/bug-description
```

### 2. 代码审查清单

在提交 Pull Request 前，检查：

- [ ] 代码符合项目规范
- [ ] 添加了必要的测试
- [ ] 测试全部通过
- [ ] 更新了相关文档
- [ ] 提交信息清晰明确
- [ ] 没有引入新的警告
- [ ] 代码有适当的注释

### 3. 版本管理

使用语义化版本（Semantic Versioning）：

- **主版本号（MAJOR）**：不兼容的 API 修改
- **次版本号（MINOR）**：向下兼容的功能性新增
- **修订号（PATCH）**：向下兼容的问题修正

示例：`1.2.3` → `1.2.4`（修复）→ `1.3.0`（新功能）→ `2.0.0`（重大变更）

### 4. 依赖管理

- 使用 `requirements.txt` 列出所有依赖
- 使用 `requirements-dev.txt` 列出开发依赖
- 定期更新依赖版本
- 锁定关键依赖的版本

### 5. 安全实践

- **不要提交敏感信息**：
  - API 密钥
  - 密码
  - 证书
  - 个人信息

- 使用 `.env.example` 提供环境变量模板
- 使用 `.gitignore` 排除敏感文件

### 6. 持续集成

配置 GitHub Actions 进行自动化测试：

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest
```

### 7. 文档维护

- 保持文档与代码同步更新
- 使用清晰的示例
- 提供常见问题解答（FAQ）
- 记录重要的设计决策

### 8. 社区管理

- 及时响应 Issue 和 PR
- 保持友好的社区氛围
- 感谢贡献者
- 定期发布更新

---

## 常见问题

### Q1: 如何处理合并冲突？

```bash
# 1. 拉取最新代码
git fetch upstream

# 2. 合并上游代码
git merge upstream/main

# 3. 解决冲突（编辑冲突文件）

# 4. 标记冲突已解决
git add .

# 5. 完成合并
git commit

# 6. 推送到远程
git push origin feature-branch
```

### Q2: 如何删除远程分支？

```bash
# 删除远程分支
git push origin --delete feature-branch

# 删除本地分支
git branch -d feature-branch
```

### Q3: 如何回滚提交？

```bash
# 回滚最后一次提交（保留更改）
git reset --soft HEAD~1

# 回滚最后一次提交（丢弃更改）
git reset --hard HEAD~1

# 回滚已推送的提交（创建新提交）
git revert HEAD
```

---

## 资源链接

- [GitHub 官方文档](https://docs.github.com/)
- [Git 官方文档](https://git-scm.com/doc)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [语义化版本](https://semver.org/)
- [PEP 8 - Python 代码风格指南](https://peps.python.org/pep-0008/)

---

## 总结

Fork 项目和规范项目管理是开源贡献的基础技能。通过遵循本教程的指导，你可以：

1. 正确地 Fork 和管理 GitHub 项目
2. 规范地组织项目结构
3. 编写清晰完整的文档
4. 遵循最佳实践进行开发

记住，良好的项目规范不仅有助于你自己，也有助于其他开发者理解和贡献你的项目。

**Happy Coding! 🚀**
