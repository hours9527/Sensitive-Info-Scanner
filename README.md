# ⚡ Sensitive Info Scanner (综合敏感信息扫描工具)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📖 项目简介

在日常渗透测试和漏洞挖掘的前期信息收集阶段，手动查找 Web 目录和挖掘 GitHub 敏感信息往往耗时巨大。
本项目是一款基于 Python 开发的自动化敏感信息扫描工具。它将前期的信息收集时间大幅缩短，通过多线程并发和多规则正则引擎，实现对目标资产的高效排查。

## ✨ 核心特性

- **🚀 多线程 Web 目录扫描**：底层采用 `ThreadPoolExecutor`，并发请求，极速探测目标站点敏感路径。
- **🛡️ 智能防误报机制**：内置软 404 (Soft 404) 动态检测，自动过滤虚假存活页面。
- **🔍 GitHub API 深度检索**：无缝对接 GitHub Code Search API，突破人工搜索的局限。
- **🧬 高危特征正则匹配**：内置数十种硬编码正则规则，精准提取无引号密码、AWS Access Key、数据库 URI 及 JWT Token。

## ⚙️ 安装与配置

1. 克隆本项目到本地：
   ```bash
   git clone [https://github.com/你的用户名/你的仓库名.git](https://github.com/你的用户名/你的仓库名.git)
   cd 你的仓库名

```

2. 安装依赖库：
```bash
pip install -r requirements.txt

```


3. **[重要]** 准备 GitHub Token：
前往 GitHub 申请 Personal Access Token，用于 GitHub 模式下的 API 认证。

## 🎯 使用指南

本工具提供统一的命令行接口，支持 `web` 和 `github` 两种模式。

### 模式一：Web 目录多线程扫描

探测目标站点是否存在敏感文件（如 `.env`, `.git`, `backup.zip` 等）。

```bash
python main.py -m web -u [http://target.com](http://target.com) -w dict.txt -t 20

```

*(参数说明：`-u` 目标 URL，`-w` 字典路径，`-t` 并发线程数)*

### 模式二：GitHub 敏感信息监控

使用正则表达式引擎，在 GitHub 开源代码中精准“狙击”泄漏的凭证。

```bash
python main.py -m github -k "filename:.env DB_PASSWORD" --token YOUR_GITHUB_TOKEN

```

*(参数说明：`-k` GitHub 高级搜索语法，`--token` 你的访问凭证)*

## ⚠️ 免责声明

1. 本工具仅面向**合法授权**的企业安全建设行为及个人学习研究目的。
2. 请勿用于任何非法或未授权的测试。因使用本工具造成的任何直接或间接后果，由使用者自行承担，原作者不负任何连带责任。

```
