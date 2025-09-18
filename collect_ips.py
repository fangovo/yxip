import requests
from bs4 import BeautifulSoup
import re
import os

urls = [
    'https://api.uouin.com/cloudflare.html',
    'https://ip.164746.xyz'
]

# IPv4正则（严格匹配0-255范围）
ipv4_pattern = re.compile(
    r'((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}'
    r'(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)'
)

# IPv6正则（支持完整和缩写 ::）
ipv6_pattern = re.compile(
    r'(([0-9a-fA-F]{1,4}:){1,7}[0-9a-fA-F]{1,4}|'
    r'([0-9a-fA-F]{1,4}:){1,7}:|'
    r'::([0-9a-fA-F]{1,4}:?){0,6}[0-9a-fA-F]{0,4})'
)

# 删除旧文件
for f in ["ipv4.txt", "ipv6.txt"]:
    if os.path.exists(f):
        os.remove(f)

ipv4_set = set()
ipv6_set = set()

for url in urls:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"请求失败 {url}：{e}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')

    if "cloudflare.html" in url or "164746.xyz" in url:
        elements = soup.find_all('tr')
    else:
        elements = soup.find_all('li')

    for element in elements:
        text = element.get_text()

        # 找IPv4
        ipv4_matches = ipv4_pattern.findall(text)
        for match in ipv4_matches:
            ip = match[0][:-1] + match[-1] if isinstance(match, tuple) else match
            ipv4_set.add(ip if isinstance(ip, str) else "".join(match))

        # 找IPv6
        ipv6_matches = ipv6_pattern.findall(text)
        for match in ipv6_matches:
            # match 是tuple，需要拼成字符串
            ip = "".join(match).strip(":")
            if ip:
                ipv6_set.add(ip)

# 保存 IPv4
with open('ipv4.txt', 'w') as f4:
    for ip in sorted(ipv4_set):
        f4.write(ip + '\n')

# 保存 IPv6
with open('ipv6.txt', 'w') as f6:
    for ip in sorted(ipv6_set):
        f6.write(ip + '\n')

print(f'提取到 {len(ipv4_set)} 个 IPv4，{len(ipv6_set)} 个 IPv6，已分别保存到 ipv4.txt 和 ipv6.txt。')
