# Obsidian2HugoBridge

## 项目描述

简化你的知识管理流程，一键从 Obsidian 导出并发布到 Hugo 网站。无需手动转换，自动化处理所有细节，让你专注于内容创作。支持最新 Obsidian 版本，并兼容多款 Hugo 主题。

## 功能特点

- **Markdown 转换**：将 Markdown 文件转换为 Hugo 兼容格式，包含自定义的提示块。
- **内容替换**：替换 Markdown 内容中指定的 URL。
- **前置参数处理**：移除 Markdown 文件前置参数中的 `url` 和 `git_commit` 字段。
- **WSL 集成**：将转换后的 Markdown 文件复制到 WSL 中 Hugo 仓库的指定目录。
- **命令执行**：一系列命令包括预览 Hugo 效果，提交仓库、更新 CDN，更新 algolia。

## 先决条件

- Python 3.7+
- WSL（Windows 子系统 Linux），基于 Debian 系列的 Linux 发行版
- 在 WSL 中安装 Hugo
- 在 WSL 中安装 Node.js（用于 Algolia 和 Tencent cloud CDN 命令）

## 安装

1. 将仓库克隆到本地机器：
    ```sh
    git clone https://github.com/raylanb/obsidian_to_hugo.git
    cd obsidian_to_hugo
    ```

2. 将代码移动到 `.obsidian\scripts\python`中
    ```sh
    cp main.py Path\.obsidian\scripts\python
    ```

3. 确保已安装和配置 WSL。在 WSL 环境中安装 Hugo 和 Node.js（如果尚未安装）。

## 配置

- **路径和 URL**：根据需要更新脚本中的路径和 URL。确保 `wsl_directory` 和 `wsl_commands` 与您的 WSL 环境和项目结构匹配。
- **配置图片域名**：`replacements` 中，左边为私人域名，右边为公开域名。
- **更换路径头部**：`convert_to_wsl_path` 中更换头部地址，比如 `G:/mydrive` 和 `//wsl.localhost/Debian`。

## 使用方法

首先安装 obsidian-python-scripter

仓库地址： [obsidian-python-scripter](https://github.com/nickrallison/obsidian-python-scripter)

前置参数模板：（尽量有 `draft`、`url`、`git_commit`，不想可以去掉，同时修改一下代码。） 

```toml
---
title: "{{title}}"
date: "{{date}}"
lastmod: "{{date}}"
draft: true
ruby: false
fraction: false
math:
  enable: false
share:
  enable: true
summary: ""
tags: 
categories:
  - ""
featuredImagePreview: 
featuredImage: 
url: 
git_commit:
---
```


然后通过 obsidian-python-scripter 运行脚本即可。

## 详细脚本描述

### 函数

- **convert_markdown(input_path, output_path)**：
  - 从 `input_path` 读取 Markdown 文件，将其转换为 Hugo 兼容格式并带 admonition 块，将结果写入 `output_path`。

- **copy_to_wsl(source_path, destination_directory)**：
  - 将文件从 `source_path` 复制到 WSL 环境中的 `destination_directory`，覆盖现有文件。

- **convert_to_wsl_path(windows_path)**：
  - 将 Windows 文件路径转换为 WSL 兼容路径。

- **extract_fields(input_path, field_names=['url', 'git_commit'])**：
  - 从 Markdown 文件的前置参数中提取指定字段。

- **execute_in_wsl(commands)**：
  - 在 WSL 环境中执行命令列表。

- **stop_hugo_server()**：
  - 停止在 WSL 中运行的 Hugo 服务器实例。

### 主脚本工作流程

1. **参数解析**：
   - 解析命令行参数以获取 vault 和特定 Markdown 文件的路径。

2. **文件路径验证**：
   - 验证指定的 Markdown 文件是否存在。

3. **字段提取**：
   - 从 Markdown 文件的前置参数中提取 `url`、`git_commit` 和 `draft` 值。

4. **Markdown 转换**：
   - 将 Markdown 文件转换为 Hugo 兼容格式。

5. **文件复制**：
   - 将转换后的 Markdown 文件复制到 WSL 中的指定目录。

6. **命令执行**：
   - 根据 `draft` 状态执行适当的 WSL 命令，包括预览或发布。

## 错误处理

- 脚本包括详细的错误处理以捕获和记录异常。错误信息会打印到控制台，并可选择记录到 `error.log` 文件。

## 贡献

欢迎通过提交问题或拉取请求为本项目做出贡献。对于重大更改，请先打开一个问题以讨论您想要更改的内容。