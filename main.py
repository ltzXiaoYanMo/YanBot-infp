from botpy import logger
from botpy.message import Message

import botpy
import json
import pathlib
import os
import yaml

curPath = os.path.dirname(os.path.realpath(__file__))
# 查找yaml配置文件
config_yaml = yaml.safe_load(open('../YanBot_infp/config.yaml', 'r', encoding='UTF-8'))

# 查找成功之后，赋值
appid = (type("bot_app_id"))
token = (type("bot_app_token"))

# 读取json文件
channel = json.loads(pathlib.Path("./json/chennel").read_text("mychannel"))
channelid = json.loads(pathlib.Path("./json/chennel").read_text("boxid"))

# 显示原Channel消息
logger.info("Bot将会运行在",channel,"频道上")
logger.warning("Bot将会运行在",channelid,"沙箱ID上")

# 测试消息，发送官方文档
class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        await message.reply(content=f"机器人的官方文档:https://bot.ymbot.top")

# 激活
intents = botpy.Intents(public_guild_messages=True)
client = MyClient(intents=intents)

# 连接腾讯QQ频道平台
client.run(appid=appid, token=token)

# 导入modules文件夹