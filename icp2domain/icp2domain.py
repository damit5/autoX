import requests
import re
import sys
import tld


def getRes(search):
    """
    发起请求，获取结果

    :param search:
    :return:
    """
    url = f"https://icplishi.com:443/{search}/"
    cookies = {"PHPSESSID": "fm3ev72l1fi0srtboqalj1esk7"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate", "Referer": "https://icplishi.com/%E4%BA%ACICP%E5%A4%871702702/",
        "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Dnt": "1", "Sec-Gpc": "1", "Te": "trailers",
        "Connection": "close"}
    resp = requests.get(url, headers=headers, cookies=cookies)
    return resp.text


if __name__ == '__main__':
    if len(sys.argv) == 2:
        domain = sys.argv[1]
        # 先通过域名获取备案号
        res = getRes(domain)
        beianNumberRegex = re.compile('<a href=".*?" target="_blank">(.*?号)-\d</a>')
        ## 备案号
        beianNumber = beianNumberRegex.findall(res)[0]

        # 再通过备案号，去查询所有的域名
        res = getRes(beianNumber)
        ## 先拿到tbody
        tbodyRegex = re.compile('<tbody>.*?</tbody>', re.S)
        tbody = tbodyRegex.findall(res)[-1]
        ## 再匹配域名，不然会有很多干扰域名
        domainRegex = re.compile('<a href="/.*?/" target="_blank">(.*?)</a>')
        allDomains = domainRegex.findall(tbody)
        allDomains = [i for i in allDomains if beianNumber not in i] # 去除备案号的干扰
        if domain in allDomains:
            allDomains = [tld.get_fld("http://" + i) for i in allDomains]  # 去除二级域名干扰
            allDomains = list(set(allDomains))  # 去重
            [print(i) for i in allDomains]
        else:
            print("bug！请提交issue")
    else:
        print(f"Usage: python3 {sys.argv[0]} domain")
