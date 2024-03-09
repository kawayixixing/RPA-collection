# Github Action推送每日新闻联播到钉钉机器人

## 新建一个私有仓库
上传脚本文件：- [XWLB-V3.0.py](脚本目录/XWLB-V3.0.py)（实现功能：每天晚上北京时间八点，对当日新闻进行摘要获取，以及每天摘要的视频地址，然后进行钉钉推送。

## 获取钉钉群机器人的token和secret
- 百度一下即可。配置到XWLB-V3.0.py中对应的位置。

## 新建一个actions
目录位置：.github/workflows/dingding-xwlb.yml
写入内容：
```
name: 钉钉推送每日新闻联播
on:
  push:
    paths:
      - '**'
  pull_request:
    paths:
      - '**'
  schedule:
    - cron: "0 20 * * *"
      timezone: Asia/Shanghai

jobs:
  run_script:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11

      - name: Install dependencies
        run: pip install requests==2.31.0 lxml==5.1.0 pytz==2024.1

      - name: Run script
        run: python demo2.py
```

# 完成
