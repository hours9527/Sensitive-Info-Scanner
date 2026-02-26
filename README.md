# ⚡ Sensitive Info Scanner & ASM Pipeline (综合敏感信息扫描与攻击面管理流水线)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📖 项目简介

本项目是一款面向企业级安全运营开发的**端到端自动化攻击面管理 (ASM) 与敏感信息扫描工具**。
从最初的单点 Web 目录扫描与 GitHub 源码泄露监控，现已进化为支持“被动资产发现 -> 数据清洗 -> 并发漏洞探测 -> JSON 报告输出”的全自动安全测试流水线。大幅降低了安全工程师在渗透测试前期的重复性信息收集工作。

## ✨ 核心模块与特性

- **🚀 自动化 ASM 流水线 (`pipeline.py`)**：一键统筹全局，实现从域名输入到漏洞输出的端到端黑盒测试。
- **🌐 被动资产发现引擎 (`subdomain_recon.py`)**：对接全球证书透明度日志 (CT Logs)，无代理、无痕迹地提取目标子域名，并内置脏数据清洗机制（如剥离误报的邮箱地址）。
- **🛡️ 多线程探测与防误报 (`dir_scanner.py`)**：底层采用 `ThreadPoolExecutor`，并内置基础软 404 (Soft 404) 动态检测，过滤虚假存活页面。
- **🔍 GitHub API 深度检索 (`github_scanner.py`)**：突破人工搜索局限，内置数十种高危正则表达式，精准提取无引号密码、AWS Access Key 及 JWT Token。

## ⚙️ 安装与配置

```bash
git clone [https://github.com/你的用户名/你的仓库名.git](https://github.com/你的用户名/你的仓库名.git)
cd 你的仓库名
pip install -r requirements.txt

```

*(注意：使用 GitHub 监控模块需在代码中配置个人 PAT)*

## 🎯 快速开始

**1. 运行完整自动化流水线 (强烈推荐):**

```bash
python pipeline.py -d target.com -w dict.txt -t 10

```

**2. 仅运行独立模块:**

```bash
# Web 目录扫描
python main.py -m web -u [http://target.com](http://target.com) -w dict.txt -t 20 -o result.json

# GitHub 源码凭证监控
python main.py -m github -k "filename:.env DB_PASSWORD"

```

## ⚠️ 免责声明

本工具仅面向**合法授权**的企业安全建设行为及个人学习研究目的。请勿用于未授权的非法测试。

```

### 第二步：Git 推送 (三连击)

确保你的 `subdomain_recon.py` 和 `pipeline.py` 都已经放在了这个文件夹里。然后在终端依次敲入这三行命令：

```bash
git add .
git commit -m "feat: Upgrade to V2.0 with ASM Pipeline and CT Logs Subdomain Recon"
git push

```

只要没报错，你的 GitHub 仓库现在就已经完美升级为 V2.0 攻击面管理兵工厂了！

这几天的实战密度极高，你不仅写出了自适应的网络防御脚本，还独立开发了具备流水线功能的自动化扫描器。要不要我帮你把这两段项目经历，按照 HR 和安全大牛最喜欢的 **STAR 法则 (情境-任务-行动-结果)** 提炼成几句精炼的话，你直接粘贴到你的求职简历里？
