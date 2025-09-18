import requests
from bs4 import BeautifulSoup
import re
import os

urls = ['https://api.uouin.com/cloudflare.html', 
        'https://ip.164746.xyz']

ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 删除旧文件
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 使用集合来去重
unique_ips = set()

for url in urls:
    try:
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'  # 确保正确编码
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 更通用的选择器，尝试多种可能包含IP的元素
        possible_elements = soup.find_all(['tr', 'td', 'li', 'p', 'div', 'span'])
        
        for element in possible_elements:
            text = element.get_text()
            ips = re.findall(ip_pattern, text)
            unique_ips.update(ips)  # 添加到集合中自动去重
            
    except Exception as e:
        print(f"处理URL {url} 时出错: {e}")

# 一次性写入所有去重后的IP
with open('ip.txt', 'w', encoding='utf-8') as file:
    for ip in sorted(unique_ips):  # 排序后写入
        file.write(ip + '\n')

print(f'找到 {len(unique_ips)} 个唯一IP地址，已保存到ip.txt文件中。')
