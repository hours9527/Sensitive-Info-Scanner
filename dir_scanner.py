import requests
import argparse
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin
import urllib3

# 禁用 requests 请求 HTTPS 时的证书警告 (安全扫描工具常用配置)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WebScanner:
    def __init__(self, target_url, threads=10):
        self.target_url = target_url if target_url.endswith('/') else target_url + '/'
        self.threads = threads
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.timeout = 5
        self.error_page_length = 0 # 用于记录软404页面的长度
        self.found_urls = []

    def _generate_random_string(self, length=12):
        """生成随机字符串，用于测试软404"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def detect_soft_404(self):
        """
        检测网站是否存在软 404 页面
        请求一个随机的不存在的路径，如果返回 200，记录其页面内容长度作为后续过滤标准
        """
        random_path = self._generate_random_string() + ".txt"
        test_url = urljoin(self.target_url, random_path)
        try:
            resp = requests.get(test_url, headers=self.headers, timeout=self.timeout, verify=False)
            if resp.status_code == 200:
                self.error_page_length = len(resp.text)
                print(f"[*] 警告: 检测到软 404 页面。基准错误页面长度为: {self.error_page_length}")
            else:
                print(f"[*] 网站无软 404 干扰，正常 404 状态码为: {resp.status_code}")
        except Exception as e:
            print(f"[-] 软 404 检测失败: {e}")

    def check_path(self, path):
        """检查单个路径"""
        path = path.strip().lstrip('/')
        if not path:
            return None
            
        url = urljoin(self.target_url, path)
        try:
            # 使用 stream=True 可以先只获取头部，对于大文件(如zip)不需要下载全部内容就能判断
            resp = requests.get(url, headers=self.headers, timeout=self.timeout, verify=False, stream=True)
            
            # 如果状态码是 200
            if resp.status_code == 200:
                # 检查是否与软 404 页面长度极为相似 (允许一点动态内容的误差)
                content_length = int(resp.headers.get('Content-Length', len(resp.content)))
                
                # 如果存在软404，且当前页面长度和软404页面长度非常接近（误差在几十字节内），则认为是误报
                if self.error_page_length > 0 and abs(content_length - self.error_page_length) < 50:
                    return None
                
                return url
        except requests.exceptions.Timeout:
            pass # 忽略超时
        except requests.exceptions.ConnectionError:
            pass # 忽略连接错误
        except Exception:
            pass
        return None

    def run(self, wordlist_path):
        """运行多线程扫描"""
        self.detect_soft_404()
        
        try:
            with open(wordlist_path, 'r', encoding='utf-8') as f:
                paths = f.readlines()
        except FileNotFoundError:
            print(f"[-] 找不到字典文件: {wordlist_path}")
            return

        print(f"[*] 加载字典成功，共 {len(paths)} 条 payload。")
        print(f"[*] 启动 {self.threads} 个线程开始扫描...")
        print("-" * 50)

        # 使用线程池并发执行
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            # 提交所有任务
            future_to_path = {executor.submit(self.check_path, path): path for path in paths}
            
            # 处理完成的任务
            for future in as_completed(future_to_path):
                result = future.result()
                if result:
                    print(f"[+] 发现敏感文件/目录: {result}")
                    self.found_urls.append(result)
        
        print("-" * 50)
        print(f"[*] 扫描结束，共发现 {len(self.found_urls)} 个敏感地址。")

if __name__ == '__main__':
    # 使用 argparse 添加命令行支持
    parser = argparse.ArgumentParser(description="Web 敏感文件扫描器的基础框架")
    parser.add_argument("-u", "--url", required=True, help="目标 URL (例如: http://example.com)")
    parser.add_argument("-w", "--wordlist", required=True, help="字典文件路径")
    parser.add_argument("-t", "--threads", type=int, default=10, help="线程数量 (默认 10)")
    
    args = parser.parse_args()

    scanner = WebScanner(target_url=args.url, threads=args.threads)
    scanner.run(wordlist_path=args.wordlist)