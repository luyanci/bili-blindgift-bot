from loguru import logger
import libs.config
import libs.live

roomcfg=libs.config.default.copy() # 偷懒，复制一份默认配置

def get_danmaku_on_gift(event:str):
    info = event['data']['data']
    giftname=info['giftName']
    name= info['uname']
    try:
        contents=str(roomcfg["chat"]["global"]["events"]['gifts'])
        content_name=contents.replace(" {user} ",f"{name}")
        contented=content_name.replace(" {gift} ",f"{giftname}")
    except:
        logger.info("Reply:"+str(contented))
    libs.live.send_danmu(text=contented)
    return

def get_danmaku_on_buyguard(event:str):
    info = event['data']['data']
    print(info)
    giftname=info['gift_name']
    name= info['username']
    num= info['num']
    try:
        contents=str(roomcfg["chat"]["global"]["events"]['guard'])
        content_name=contents.replace(" {user} ",f"{name}")
        content_num=content_name.replace(" {type} ",f"{giftname}")
        contented=content_num.replace(" {num} ",f"{num}")
    except:
        logger.info("Reply:"+str(contented))
    libs.live.send_danmu(text=contented)
    return