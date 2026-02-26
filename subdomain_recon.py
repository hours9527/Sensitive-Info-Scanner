import requests
import argparse

def get_subdomains_from_crtsh(domain):
    """
    通过 crt.sh 接口获取目标域名的子域名
    """
    print(f"[*] 🌐 正在连接全球证书透明度日志库 (crt.sh)...")
    print(f"[*] 🔍 目标: {domain} (这可能需要十几秒，请耐心等待)")
    
    # 构造 API 请求，查询特定域名，返回 JSON 格式
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'application/json'
    }
    
    # 使用 set (集合) 来自动去重
    subdomains = set()

    try:
        resp = requests.get(url, headers=headers, timeout=30)
        
        if resp.status_code == 200:
            data = resp.json()
            for entry in data:
                # crt.sh 返回的 name_value 包含了域名信息
                name_value = entry.get('name_value', '')
                
                # 有些证书包含多个域名，用换行符隔开，我们需要切分
                for sub in name_value.split('\n'):
                    sub = sub.strip().lower()
                    # 过滤掉泛域名 (比如 *.target.com) 和不相关的域名
                    if sub.endswith(domain) and not sub.startswith('*') and '@' not in sub:
                        subdomains.add(sub)
            
            print(f"[+] 🎉 发现 {len(subdomains)} 个唯一子域名！")
            return list(subdomains)
        else:
            print(f"[-] API 请求失败，状态码: {resp.status_code}")
            
    except requests.exceptions.Timeout:
        print("[-] ⏳ 请求超时，crt.sh 服务器可能较拥挤，请稍后再试。")
    except Exception as e:
        print(f"[-] ❌ 发生错误: {e}")
        
    return []

def main():
    parser = argparse.ArgumentParser(description="子域名自动化发现引擎")
    parser.add_argument("-d", "--domain", required=True, help="目标主域名 (例如: example.com)")
    parser.add_argument("-o", "--output", help="导出结果的文件路径 (例如: subdomains.txt)")
    
    args = parser.parse_args()
    
    results = get_subdomains_from_crtsh(args.domain)
    
    if results:
        # 打印前 10 个展示一下
        print("\n[*] 部门资产展示 (Top 10):")
        for sub in results[:10]:
            print(f"    - {sub}")
            
        # 如果指定了导出文件，则保存结果
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                for sub in results:
                    f.write(sub + '\n')
            print(f"\n[+] 💾 所有资产已成功保存至: {args.output}")

if __name__ == "__main__":
    main()