import os
import json
from loguru import logger
from bilibili_api import Credential,login,user,sync
from . import config

def _user_login():
    import tkinter as tk
    a = login.login_with_qrcode(tk.Tk())
    return a

def _user_login_term():
    a = login.login_with_qrcode_term()
    return a

async def user_info(uid:int,Credential: Credential):
    u = user.User(uid=uid,credential=Credential)
    info = await u.get_user_info()
    return info

def get_self_uid(Credential: Credential):
    i= sync( user.get_self_info(credential=Credential))
    bot_uid=str(i['mid'])
    return bot_uid

def user_login():
    global c
    logger.info('Try to login from cookie.json...')
    try:
        cook=json.load(open(file=f"./cookie.json"))
        c = Credential(sessdata=cook["SESSDATA"],bili_jct=cook["bili_jct"],buvid3=cook["buvid3"],ac_time_value=cook["ac_time_value"],dedeuserid=cook["DedeUserID"])
    except:
        logger.info('Failed!Please login with qrcode!')
        try:
            c = _user_login()
        except ModuleNotFoundError:
            c = _user_login_term()
        try:
            c.raise_for_no_sessdata()
            c.raise_for_no_bili_jct()
            coco=json.dumps(c.get_cookies(),ensure_ascii=False)
        except:
            logger.exception("Login error!")
            os._exit(1)
        finally:
            with open(file="./cookie.json",mode="w",encoding="utf-8",errors="ignore") as cookies:
                cookies.write(coco)
    get_self_uid(c)
    logger.info('Login successfully!')
    return c