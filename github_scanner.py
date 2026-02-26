import requests
import re
import time

class GitHubScanner:
    def __init__(self, token):
        # GitHub API 需要身份认证，否则会被严重限速
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.api_url = "https://api.github.com/search/code"
        
        # 【简历核心亮点】：正则表达式规则字典
        self.regex_rules = {
            # 1. AWS Access Key ID (特征极其明显，通常以 AKIA 开头，后接 16 位大写字母或数字)
    'AWS_Access_Key': r'AKIA[0-9A-Z]{16}',

    # 2. 通用密码/密钥提取 (兼容 password=xxx, pwd : 'xxx', secret_key="xxx")
    # 解释:
    # (?i) 忽略大小写
    # (?:...) 非捕获分组，匹配 password/passwd/pwd/secret/key/token
    # \s*[:=]\s* 匹配等号或冒号，两边允许有空格
    # [\'"]? 匹配可能存在的单/双引号
    # ([^\s\'"]+) 核心捕获组：提取不包含空格和引号的实际密码内容
    'Generic_Password': r'(?i)(?:password|passwd|pwd|secret|key|token)\s*[:=]\s*[\'"]?([^\s\'"]+)[\'"]?', 

    # 3. 常见的 JDBC/MySQL 数据库连接字符串 (提取账号密码)
    'Database_URI': r'(?i)(?:mysql|postgresql|jdbc:\w+)://([a-zA-Z0-9_]+):([a-zA-Z0-9_!@#$%^&*]+)@[a-zA-Z0-9_\.-]+',

    # 4. JWT Token (现代 Web 应用极易泄露，特征是三个部分由点隔开，以 ey 开头)
    'JWT_Token': r'ey[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}'
        }
        self.results = []

    def search(self, keyword, limit=5):
        print(f"[*] 正在 GitHub API 搜索关键字: {keyword}")
        # q=关键字, per_page=每次返回数量
        params = {'q': keyword, 'per_page': limit} 
        try:
            resp = requests.get(self.api_url, headers=self.headers, params=params)
            if resp.status_code == 200:
                items = resp.json().get('items', [])
                print(f"[*] 找到 {len(items)} 个相关文件，正在下载源码并进行正则匹配...")
                
                for item in items:
                    self._analyze_code(item)
                    # 极其重要：延迟 1-2 秒，防止触发 GitHub 滥用检测被封 IP
                    time.sleep(1.5) 
            else:
                print(f"[-] API 请求失败，状态码: {resp.status_code}, 返回信息: {resp.text}")
        except Exception as e:
            print(f"[-] 网络请求发生错误: {e}")

    def _analyze_code(self, item):
        """拉取原始代码并用正则表达式匹配"""
        # 将普通的 GitHub 网页 URL 转换成 raw 格式，这样拿到的直接是代码纯文本
        raw_url = item['html_url'].replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
        
        try:
            resp = requests.get(raw_url, timeout=5)
            if resp.status_code == 200:
                content = resp.text
                
                # 遍历正则规则字典进行匹配
                for rule_name, pattern in self.regex_rules.items():
                    matches = re.findall(pattern, content)
                    if matches:
                        print(f"\n[+] 🚨 【高危泄漏】在文件 {item['name']} 中发现 {rule_name}!")
                        print(f"    来源 URL: {item['html_url']}")
                        match_list = []
                        
                        # 打印匹配结果 (做脱敏处理，展现安全从业者的专业素养)
                        for m in set(matches[:3]): # 只取前3个去重后的结果
                            # 如果是元组（正则中有括号分组），取第一个元素
                            m_str = m if isinstance(m, str) else m[0]
                            # 脱敏展示：只显示前3位和后3位
                            masked = f"{m_str[:3]}***{m_str[-3:]}" if len(m_str) > 6 else "***"
                            print(f"    命中内容: {masked}")
                            match_list.append(masked)
                        self.results.append({"rule_hit": rule_name,
                            "file_name": item['name'],
                            "source_url": item['html_url'],
                            "matches": match_list})
        except Exception:
            pass # 忽略抓取源码时的网络错误

if __name__ == "__main__":
    # ⚠️ 在这里填入你的 GitHub Personal Access Token
    GITHUB_TOKEN = "YOUR_GITHUB_TOKEN_HERE" 
    
    if GITHUB_TOKEN == "YOUR_GITHUB_TOKEN_HERE":
        print("[-] 运行失败：请先去 GitHub 申请并填入你的 Personal Access Token！")
    else:
        scanner = GitHubScanner(GITHUB_TOKEN)
        # 演示：在全局搜索名为 .env 的文件，且里面包含 DB_PASSWORD 关键字的代码
        scanner.search("filename:.env DB_PASSWORD", limit=3)