from botpy import logger

import yaml
import sys
import json
import portalocker


def safe_file_read(filename: str, encode: str = "UTF-8", mode: str = "r") -> str or bytes:
    if mode == 'r':
        with open(filename, mode, encoding=encode) as file:
            portalocker.lock(file, portalocker.LOCK_EX)
            tmp = file.read()
            portalocker.unlock(file)
    else:
        with open(filename, mode) as file:
            portalocker.lock(file, portalocker.LOCK_EX)
            tmp = file.read()
            portalocker.unlock(file)

    return tmp


def safe_file_write(filename: str, s, mode: str = "w", encode: str = "UTF-8"):
    if 'b' not in mode:
        with open(filename, mode, encoding=encode) as file:
            portalocker.lock(file, portalocker.LOCK_EX)
            file.write(s)
            portalocker.unlock(file)
    else:
        with open(filename, mode) as file:
            portalocker.lock(file, portalocker.LOCK_EX)
            file.write(s)
            portalocker.unlock(file)


try:
    config_yaml = yaml.load(open('config.yaml', encoding='UTF-8'), Loader=yaml.FullLoader)
except FileNotFoundError:
    safe_file_write('config.yaml', """count_ban: 4  # 木鱼调用频率限制
# 注意：腾讯云内容安全 API 收费为 0.0025/条
text_review: false  # 是否使用腾讯云内容安全 API 对文本内容进行审核：true -> 是 | false -> 否，使用本地敏感词库
# 请参考此文章就近设置地域：https://cloud.tencent.com/document/api/1124/51864#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8
Region: ap-hongkong  # 使用香港地区 API
enable_mysql: false  # 是否使用MySQL存储数据
oneword: https://v1.hitokoto.cn/?c=f&encode=text # 一言api
    """)
    logger.error(
        'config.yaml 文件不存在，已生成默认配置文件，请修改后重新运行。'
    )
    sys.exit(1)

try:
    cloud_config_json = json.load(open('config.json', 'r', encoding='UTF-8'))
except FileNotFoundError:
    safe_file_write('cloud.json', """{
  "qq_bot_id": "",
  "qq_bot_token": "",
  "qq_bot_passwd": "",
  "qq_api": "https://api.sgroup.qq.com/",
  "count_ban": 5,
  "text_review": "false",
  "Region": "ap_nanjing"
}""")
    logger.error(
        'config.json 未创建，程序已自动创建')
    sys.exit(1)


def get_config(name: str):
    try:
        return config_yaml[name]
    except KeyError:
        logger.error(f'{name} 在配置文件中找不到')
        return None


def get_cloud_config(name: str):
    try:
        return cloud_config_json[name]
    except KeyError:
        logger.error(f'{name} 在配置文件中找不到')
        return ""
