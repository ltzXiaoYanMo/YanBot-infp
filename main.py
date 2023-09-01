from botpy import logger
from botpy.message import Message

import botpy
import yaml
import json

# 测试消息，发送官方文档
class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        await message.reply(content=f"机器人的官方文档:https://bot.ymbot.top")