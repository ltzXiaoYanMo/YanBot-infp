from botpy import logger
from botpy.message import Message

import botpy
import json
import pathlib

# 读取json文件
channel = json.loads(pathlib.Path("./json/chennel").read_text("mychannel"))
channelid = json.loads(pathlib.Path("./json/chennel").read_text("boxid"))

# 测试消息，发送官方文档
class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        await message.reply(content=f"机器人的官方文档:https://bot.ymbot.top")