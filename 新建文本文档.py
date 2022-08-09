import requests
from lxml import etree

headers = {
    "Usser-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36"
}


def check_ip(proxies_list):
    can_use = []
    for i in proxies_list:
        try:
            response = requests.get(base_url, headers=headers, proxies=i, timeout=0.5)  # 设置代理ip，并且设置请求超时时间
            if response.status_code == 200:
                can_use.append(i)

        except Exception:
            print(i,'--检验不通过--')
        finally:
            print("--质量检验通过的ip--",i)
    return can_use




proxies_list = []

for i in range(2, 10):    
    print("正在爬{}页的数据".format(i))
    base_url = "http://www.ip3366.net/free/?stype=1&page={}".format(str(i))
    response = requests.get(base_url, headers=headers).text
    tree = etree.HTML(response)
    ip_list = tree.xpath("//div[@id='list']/table/tbody/tr")  # 拿到代理IP的列表

    for tr in ip_list:
        http_type = tr.xpath("./td[4]/text()")[0]  # xpath返回列表类型，加上索引就是字符串
        ip = tr.xpath('./td[1]/text()')[0]
        port = tr.xpath('./td[2]/text()')[0]
        proxies_dict = {}  # 构建代理ip的结构
        proxies_dict[http_type] = ip + ":" + port
        proxies_list.append(proxies_dict)  # 加入一个空列表
    can_use = check_ip(proxies_list)
    print("检验ip合格的数量:",len(can_use))








