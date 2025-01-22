import os
import datetime
from loguru import logger
from bilibili_api import sync
from libs import config
from libs import live,user
from libs import blind,gift,data

data.init()

def listen():
    live.set(config.room,user.c)
    
    @live.LiveDanma.on('VERIFICATION_SUCCESSFUL')
    async def on_successful(event):
        # 连接成功
        logger.info('Connected!')
        await live.send_danmu(text="connected!")
        logger.debug(event)
        return
    
    @live.LiveDanma.on('GUARD_BUY')
    async def on_guard_buy(event:str):
        gift.get_danmaku_on_buyguard(event)
        return
    
    @live.LiveDanma.on("SEND_GIFT")
    async def events(event:str):
        if blind.check_blind(event):
            blind.on_blind(event)
            data.save_for_blind_gift(event)
            return
        else:
            gift.get_danmaku_on_gift(event)
            data.save(event)
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