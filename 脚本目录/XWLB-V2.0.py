import time
import csv
import os
# 1. 导入 WebBotMain 类
from AiBot import WebBotMain # Python版本需要大于3.10，需要安装pip install aibot
# 对当天的新闻联播摘要进行抓取，获取完整版视频链接、摘要。获取节主要内容和链接和节文字内容。

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
        print("开始")

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

        # 获取完整版视频链接
        xpath5 = '//*[@id="content"]/li[1]/a'
        content5 = self.get_element_attr(xpath5,'href')
        content5 = "完整版视频链接：" + content5

        # 指定路径下创建一个CSV文件并写入内容
        directory = 'C:/Users/xxx/Nutstore/1/300Work/302文档/30202收集/3020201一鲸/新闻联播专场/3'  # 替换为你想要保存的目录路径
        filename = '{}.csv'.format(file_name)
        # filename = 'test.csv'
        # 创建完整的文件路径
        file_path = os.path.join(directory, filename)



        with open(file_path, 'a', newline='', encoding='utf-8') as csvfile: #追加写入
            writer = csv.writer(csvfile)
            data_array = [file_name + '新闻联播主要内容摘要：']  # 创建一个空数组，用于存放摘要内容
            # 循环进入每一个子视频，获取到内容后退出
            for i in range(2, 31):
                # 进入一个标签页
                xpath2 = '//*[@id="content"]/li[{}]/div/a'.format(i) 
                content2 = self.get_element_attr(xpath2,'href')
                self.goto(content2)
                # 判断链接是否为空，为空则退出
                if content2 is None:
                    break
                else:
                    # 获取本节视频链接
                    content2 = "节视频链接：" + content2

                    # 获取摘要内容
                    xpath3 = '//*[@id="page_body"]/div[1]/div[2]/div[2]/div[2]/div/ul/li[1]/p'
                    content3 = self.get_element_text(xpath3)
                    data_array.append(content3)  # 将数据添加到数组中
                    content3 = "节摘要：" + content3 

                    # 获取全部文字内容
                    xpath4= '//*[@id="content_area"]'
                    content4 = self.get_element_text(xpath4)
                    content4 = "节全文内容：" + content4

                    # 将每个标签页获取到内容，写入csv
                    content_list = [content3, content2, content4]
                    rows = [[content] for content in content_list]

                     # 使用 writerows() 方法写入多行内容
                    writer.writerows(rows)

                    # 返回上一页
                    self.back()
        print("写入完成")

        # 加入完整版视频链接
        data_array.append(content5)

        # 将总结的摘要写入最开始的行
        # 读取已有的 CSV 文件
        existing_data = []
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                existing_data.append(row)

        # 将新数据插入到已有的 CSV 文件的首行
        # 逐行读取已有数据，并将其添加到新的列表中
        updated_data = [data_array] + existing_data

        # 将更新后的数据写入到新的 CSV 文件或覆盖原始文件
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(updated_data)
        print("更新完成")


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
