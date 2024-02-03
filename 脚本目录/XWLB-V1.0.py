import time
import csv
import os
# 1. 导入 WebBotMain 类
from AiBot import WebBotMain # Python版本需要大于3.10，需要安装pip install aibot
# 对当天的新闻联播主要内容进行抓取，并生成以新闻联播播出时间为准的csv文件，
# 同时打开完整版新闻联播并播放。V1.0

# 2. 自定义一个脚本类，继承 WebBotMain
class CustomWebScript(WebBotMain):
    # 3. 设置等待参数
    # 3.1 设置等待时间
    wait_timeout = 3
    # 3.2 设置重试间隔时长
    interval_timeout = 0.5
    # 注意：此方法是脚本执行入口
    def script_main(self):
        # 打开浏览器进入CCTV的页面
        self.goto("https://tv.cctv.com/lm/xwlb/")
        time.sleep(3)
        # 获取新闻时间作为csv的文件名
        xpath = '//*[@id="content"]/li[1]/a'
        content = self.get_element_text(xpath)
        if content is not None and len(content) >= 24:
            file_name = content[10:24] # 提取时间字段
            file_name = file_name.replace(':', '') # 去除:
            file_name = file_name.replace(' ', '') # 去除空格，最后拼接后的时间字段为202402022100
            print(file_name) 
        else:
            file_name = 'output' # 默认文件名

        # 指定路径下创建一个CSV文件并写入内容
        directory = 'C:/Users/xxx/300Work/302文档/30202收集/3020201一鲸/新闻联播专场/2'  # 替换为你想要保存的目录路径
        filename = '{}.csv'.format(file_name)

        # 创建完整的文件路径
        file_path = os.path.join(directory, filename)

        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for i in range(2, 31):
                xpath = '//*[@id="content"]/li[{}]/a'.format(i)
                content = self.get_element_text(xpath)
                if content is None:
                    break
                else:# 删除[视频]这几个字符
                    content = content[4:]  # 删除前三个字符
                    writer.writerow([content])  # 写入内容

        # 播放完整版今日新闻联播视频内容
        xpath = '//*[@id="content"]/li[1]/a'
        self.click_element(xpath)

# 7. 执行脚本，Pycharm 中，直接右键执行
if __name__ == '__main__':
    # 启动脚本，监听 9999 号端口
    # 默认使用 Chrome 浏览器

    # local=True 时，是本地运行脚本，会自动启动 WebDriver.exe 驱动；
    # 在远端部署脚本时，请设置 local=False，手动启动 WebDriver.exe，启动 WebDriver.exe 时需指定远端 IP 或端口号；

    # 如本地部署脚本，需要传递 WebDriver 启动参数时，参考下面方式，如不需传递启动参数，则忽略：
    driver_params = {
        "browserName": "chrome",
        "debugPort": 0,
        "userDataDir": "UserData",
        "browserPath": None,
        "argument": None,
    }
    CustomWebScript.execute(9999, local=True, driver_params=driver_params)
