import requests
from lxml import etree
import datetime
import pytz
import json
import hashlib
import base64
import hmac
import os
import time
from urllib.parse import quote_plus
# 使用get请求获取新闻联播主要内容。使用钉钉推送.每天晚上8:00北京时间执行一次.

class Messenger:
    def __init__(self, token=None, secret=None):
        self.timestamp = str(round(time.time() * 1000))
        self.URL = 'https://oapi.dingtalk.com/robot/send'
        self.headers = {'Content-Type': 'application/json'}
        self.token = token or os.getenv('DD_ACCESS_TOKEN')
        self.secret = secret or os.getenv('DD_SECRET')
        self.sign = self.generate_sign()
        self.params = {'access_token': self.token, 'sign': self.sign}

    def generate_sign(self):
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(self.timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        return quote_plus(base64.b64encode(hmac_code))   
    # md
    def send_md(self, title, text):
        data = {
            'msgtype': 'markdown',
            'markdown': {
                'title': title, 
                'text': text}
        }
        self.params['timestamp'] = self.timestamp
        return requests.post(
            url=self.URL,
            data=json.dumps(data),
            params=self.params,
            headers=self.headers
        )

# 定义一个函数获取数据当前时间和ISO 8601时间
def get_current_time():
    # 获取当前时间
    current_time = datetime.datetime.now()

    # 设置时区为北京时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    beijing_time = current_time.astimezone(beijing_tz)

    # 获取"20240309"格式的日期
    date_format = beijing_time.strftime('%Y%m%d')

    # 获取ISO 8601格式的时间
    iso_format = beijing_time.strftime('%Y-%m-%dT%H:%M:%S%z')

    return date_format, iso_format

def parse_html(url):
    # 发起网站请求
    response = requests.get(url)
    
    # 设置编码方式为 UTF-8
    response.encoding = 'utf-8'
    
    # 解析返回的 HTML 数据
    html = etree.HTML(response.text)
    
    return html

# 访问主站
url1 = "https://tv.cctv.com/lm/xwlb/"
html = parse_html(url1)

# 构建XPath表达式并计算 <div> 下的 <li> 元素数量，统计有多少个子章节。
xpath = 'count(//*[@id="content"]/li)'
count = int(html.xpath(xpath))

# 调用函数获取当前时间
date, iso_time = get_current_time()
arry_text = []
# 循环获取每个视频的链接。
for i in range(2, count + 1):
    xpath2 = '//*[@id="content"]/li[{}]/div/a/@href'.format(i) 
    urls = html.xpath(xpath2)
    # 循环访问每个节视频的链接,获取节摘要内容.
    for url2 in urls:
        sub_html = parse_html(url2)  
        xpath3 = '//*[@id="page_body"]/div[1]/div[2]/div[2]/div[2]/div/ul/li[1]/p/text()' #节摘要
        content3 = sub_html.xpath(xpath3)
        url = "[完整版视频链接]({})".format(urls[0]) 
        content3 = '[节摘要：' + ''.join(content3) + ']({})'.format(url2)      
        # content_str = '\n'.join(content3)
        arry_text.append(content3 + '\n')

# 这里的token和secret替换为自己的钉钉群内机器人的信息。
m = Messenger(
    token='哈利',
    secret='路亚'
)

title = date + "新闻联播"
text =  '\n'.join(arry_text)
m.send_md(title, text)
