import os
import datetime
from loguru import logger
from bilibili_api import sync

from libs import config
from libs import live,user
from libs import blind

def listen():
    live.set(config.room,user.c)
    
    @live.LiveDanma.on('VERIFICATION_SUCCESSFUL')
    async def on_successful(event):
        # 连接成功
        logger.info('Connected!')
        await live.send_danmu(text="connected!")
        logger.debug(event)
        return
    
    
    
    @live.LiveDanma.on("SEND_GIFT")
    async def events(event:str):
        if blind.check_blind(event) is True:
            await blind.on_blind(event)
        else:
            return
    
    try:
        sync(live.LiveDanma.connect())
    finally:
        os._exit(0)
    
    
@logger.catch
def main():
    today=datetime.date.today()
    logger.add(f"logs/log-{today}.log",rotation="1 day",encoding="utf-8",format="{time} {level}-{function} {message}")
    logger.info("Starting...")
    user.user_login()
    config.loadroomcfg()
    listen()

if __name__ == "__main__":
    main()