#!/usr/bin/env python
# 给定一个IP列表文件，如果IP一个段的个数超过20，就整理为C段，否则保留原来的IP
import sys
import ipaddress
import re

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} ipList.txt")
        exit(0)
    with open(sys.argv[1], 'r') as f:
        res = f.readlines()

    tmpIp = []  # 临时保存所有去除最后一个 . 的IP
    tmpIpNoDuplicate = []  # 临时保存所有去除最后一个 . 的IP并去重
    tmpIpTimes = {}  # 临时保存所有去除最后一个 . 的IP出现次数
    resIp = [] # 最终结果IP

    # 验证IP合法性，不是IP的就删除
    compile_ip = re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    res = [ip for ip in res if compile_ip.match(ip.strip("\n"))]

    # 获取所有去除最后一个 . 的IP
    for ip in res:
        # 去掉内网IP
        if not ipaddress.ip_address(ip.strip()).is_private:
            tmpIp.append(".".join(ip.split(".")[:3]))
    # 去重
    tmpIpNoDuplicate = list(set(tmpIp))
    # 统计次数
    for ip in tmpIpNoDuplicate:
        tmpIpTimes[ip] = tmpIp.count(ip)
    # 结果生成
    for ip in tmpIpTimes:
        if tmpIpTimes.get(ip) >= 20:
            [resIp.append(ip + f".{i}") for i in range(1, 255)]
        else:
            [resIp.append(t_ip.strip("\n")) for t_ip in res if ip in t_ip]

    [print(ip) for ip in resIp]
