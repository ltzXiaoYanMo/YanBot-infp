from loguru import logger

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
        'config.json 未创建，程序已自动创建，请参考 https://config.ymbot.top 填写该文件的内容')
    sys.exit(1)