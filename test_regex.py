import re

# 模拟我们从 GitHub 上抓取到的 .env 或 config.php 源码内容
mock_github_code = """
# Database Config
DB_HOST = 127.0.0.1
db_password=my_super_secret_db_pass_123
MYSQL_URI="mysql://root:Admin@12345@localhost:3306/mydb"

# Cloud Provider
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# API Settings
API_TOKEN : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
"""

regex_rules = {
    'AWS_Access_Key': r'AKIA[0-9A-Z]{16}',
    'Generic_Password': r'(?i)(?:password|passwd|pwd|secret|key|token)\s*[:=]\s*[\'"]?([^\s\'"]+)[\'"]?',
    'Database_URI': r'(?i)(?:mysql|postgresql|jdbc:\w+)://([a-zA-Z0-9_]+):([a-zA-Z0-9_!@#$%^&*]+)@[a-zA-Z0-9_\.-]+',
    'JWT_Token': r'ey[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}'
}

print("[*] 开始正则匹配测试...\n")

for rule_name, pattern in regex_rules.items():
    # 使用 re.IGNORECASE 是另一种忽略大小写的方式，但我们在正则里加了 (?i)，所以直接 findall 即可
    matches = re.findall(pattern, mock_github_code)
    
    if matches:
        print(f"[+] 命中规则: {rule_name}")
        for match in matches:
            # 如果正则中有多个括号分组，match 会是一个元组 (比如账号, 密码)
            if isinstance(match, tuple):
                print(f"    -> 提取内容: 账号 '{match[0]}', 密码 '{match[1]}'")
            else:
                print(f"    -> 提取内容: {match}")
    else:
        print(f"[-] 规则 {rule_name} 未匹配到内容")