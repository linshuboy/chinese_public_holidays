# -*- coding: utf-8 -*-
import json
import datetime

HELLO_WORLD = b'Hello world!\n'


def handler(environ, start_response):
    context = environ['fc.context']
    request_uri = environ['fc.request_uri']
    for k, v in environ.items():
        if k.startswith('HTTP_'):
            pass
            # process custom request headers
    # do something here
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    # 通过读取文件holidays.json获取json文件,并转换为python对象,不存在则返回空json
    try:
        with open('all_holidays.json', 'r', encoding='utf-8') as f:
            holidays = json.load(f)
    except:
        holidays = {}
    # 获取当前时间
    now = datetime.datetime.now()
    # 获取当前时间字符串
    now_str = now.strftime('%Y%m%d')
    if now_str in holidays:
        if now_str in holidays and 'work' in holidays[now_str] and holidays[now_str]['work']:
            return [b'work']
        else:
            return [b'holiday']
    else:
        now_weekday = now.weekday()
        if now_weekday == 5 or now_weekday == 6:
            return [b'holiday']
        else:
            return [b'work']
