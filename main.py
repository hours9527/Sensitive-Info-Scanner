import argparse
import time
import sys
import json

# 导入你写好的两个模块
try:
    from dir_scanner import WebScanner
    from github_scanner import GitHubScanner
except ImportError as e:
    print(f"[-] 模块导入失败，请确保 dir_scanner.py 和 github_scanner.py 在同一目录下。\n报错信息: {e}")
    sys.exit(1)

def print_banner():
    banner = """
    ==================================================
      ⚡ Sensitive Info Scanner V1.0 ⚡
      Author: YourName | 针对 Web 目录 & GitHub 泄漏检测
    ==================================================
    """
    print(banner)

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description="综合敏感信息扫描工具")
    
    # 核心参数：选择模式
    parser.add_argument("-m", "--mode", choices=['web', 'github'], required=True, help="选择扫描模式 (web 或 github)")
    parser.add_argument("-o", "--output", help="导出 JSON 报告的文件路径 (例如: result.json)")
    # Web 扫描组
    web_group = parser.add_argument_group("Web 扫描参数")
    web_group.add_argument("-u", "--url", help="目标 URL (例如: http://example.com)")
    web_group.add_argument("-w", "--wordlist", help="字典文件路径")
    web_group.add_argument("-t", "--threads", type=int, default=10, help="线程数量 (默认 10)")
    
    # GitHub 扫描组
    gh_group = parser.add_argument_group("GitHub 扫描参数")
    gh_group.add_argument("-k", "--keyword", help="GitHub 搜索关键字 (例如: 'filename:.env db_password')")
    gh_group.add_argument("--token", help="GitHub Personal Access Token")

    args = parser.parse_args()
    start_time = time.time()
    report_data = {
        "scan_mode": args.mode,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "findings": []
    }

    # 逻辑分支
    if args.mode == 'web':
        if not args.url or not args.wordlist:
            print("[-] 错误：Web 模式下必须提供 -u 和 -w 参数！")
            sys.exit(1)
        print(f"[*] 🚀 启动 Web 目录敏感文件扫描模式 | 目标: {args.url}")
        scanner = WebScanner(target_url=args.url, threads=args.threads)
        scanner.run(wordlist_path=args.wordlist)
        report_data["target"] = args.url
        report_data["findings"] = scanner.found_urls
    elif args.mode == 'github':
        if not args.keyword or not args.token:
            print("[-] 错误：GitHub 模式下必须提供 -k 和 --token 参数！")
            sys.exit(1)
        print(f"[*] 🚀 启动 GitHub 敏感信息监测模式 | 关键字: {args.keyword}")
        scanner = GitHubScanner(token=args.token)
        # 这里默认跑前 5 个结果，你可以根据需要调整
        scanner.search(keyword=args.keyword, limit=5)
        report_data["keyword"] = args.keyword
        report_data["findings"] = scanner.results

    end_time = time.time()
    time_cost = round(end_time - start_time, 2)
    print(f"\n[*] 扫描任务结束！总耗时: {time_cost} 秒")
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                # indent=4 让 JSON 文件有漂亮的缩进格式，ensure_ascii=False 支持中文正常显示
                json.dump(report_data, f, indent=4, ensure_ascii=False)
            print(f"[+] 📊 完美！扫描报告已成功导出至: {args.output}")
        except Exception as e:
            print(f"[-] 报告导出失败: {e}")

if __name__ == "__main__":
    main()