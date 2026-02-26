import time
import argparse
# 导入你写好的两个模块
from subdomain_recon import get_subdomains_from_crtsh
from dir_scanner import WebScanner

def run_pipeline(domain, wordlist, threads):
    print("==================================================")
    print("  🚀 启动自动化攻击面测绘与扫描流水线 (ASM Pipeline)")
    print(f"  🎯 目标主域: {domain}")
    print("==================================================\n")
    
    start_time = time.time()

    # ---------------------------------------------------------
    # 阶段 1：资产发现 (Reconnaissance)
    # ---------------------------------------------------------
    print("[阶段 1] 开始从全网证书透明度日志收集子域名...")
    subdomains = get_subdomains_from_crtsh(domain)
    
    if not subdomains:
        print("[-] 未发现有效子域名，流水线终止。")
        return

    # ---------------------------------------------------------
    # 阶段 2：自动化探测 (Vulnerability Scanning)
    # ---------------------------------------------------------
    print(f"\n[阶段 2] 将对存活的 {len(subdomains)} 个资产进行并发敏感目录扫描...")
    print("  (注：实战中通常会先进行端口存活探测，此处为了演示直接尝试 HTTP 请求)")
    
    all_vuln_urls = []
    
    # 遍历每一个扫出来的子域名，喂给目录扫描器
    # 为了测试速度，这里我们只取前 5 个子域名演示
    test_limit = 5 
    for sub in subdomains[:test_limit]:
        target_url = f"http://{sub}"
        print(f"\n[*] 👉 正在扫描节点: {target_url}")
        
        # 调用我们之前写的 WebScanner 类
        scanner = WebScanner(target_url=target_url, threads=threads)
        scanner.run(wordlist_path=wordlist)
        
        if scanner.found_urls:
            all_vuln_urls.extend(scanner.found_urls)

    # ---------------------------------------------------------
    # 阶段 3：结果汇总 (Reporting)
    # ---------------------------------------------------------
    end_time = time.time()
    print("\n==================================================")
    print("  🏁 流水线执行完毕！")
    print(f"  ⏱️  总耗时: {round(end_time - start_time, 2)} 秒")
    print(f"  🚨 共发现在线敏感资产: {len(all_vuln_urls)} 个")
    
    for url in all_vuln_urls:
        print(f"      - {url}")
    print("==================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="端到端自动化安全测试流水线")
    parser.add_argument("-d", "--domain", required=True, help="目标主域 (如: example.com)")
    parser.add_argument("-w", "--wordlist", required=True, help="敏感目录字典路径")
    parser.add_argument("-t", "--threads", type=int, default=5, help="单个节点的并发线程数")
    
    args = parser.parse_args()
    run_pipeline(args.domain, args.wordlist, args.threads)