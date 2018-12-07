#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""blog：http://www.cnblogs.com/suoning"""
__author__ = 'Nick Suo'

import tornado.web
import tornado.ioloop

import time
import hashlib

container = {}   # 用于存放 Session，可放在数据库，缓存等地

class Session:

    def __init__(self,handler):
        """
        :param handler: 在 initialize 方法函数里初始化，传入当前对象self
        :param handler: 客户端是否有指定 __ss__ flag
        """
        self.handler = handler
        self.random_str = None

    def __genarte_randmo_str(self):
        """
        以当前时间戳生成随机字符串
        :return: 返回随机字符串
        """
        obj = hashlib.md5()
        obj.update(bytes(str(time.time()), encoding='utf-8'))
        random_str = obj.hexdigest()
        return random_str

    def __setitem__(self,key,value):
        """
        设置 session 方法函数
        :param key: 设置的 key
        :param value: 设置的 value
        """
        if not self.random_str:
            random_str = self.handler.get_secure_cookie("__ss__")
            if not random_str:
                random_str = self.__genarte_randmo_str()
                container[random_str] = {}
            else:
                if random_str not in container.keys():
                    random_str = self.__genarte_randmo_str()
                    container[random_str] = {}
            self.random_str = random_str

        container[self.random_str][key] = value
        self.handler.set_secure_cookie("__ss__",self.random_str)    # expires_days=None

    def __getitem__(self,key):
        """
        获取指定 session 方法函数
        :param key: 要获取的 key
        :return: 返回获取到的值
        """
        randmon_str = self.handler.get_secure_cookie("__ss__")
        randmon_str = str(randmon_str,encoding='utf-8')
        if not randmon_str:
            return None
        user_info_dic = container.get(randmon_str, None)
        if not user_info_dic:
            return None
        value = user_info_dic.get(key, None)
        return value


class MyHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.session = Session(self)


class IndexHandler(MyHandler):

    def get(self, *args, **kwargs):
        ......
        result = self.session["name"]    # 获取 Session 方法函数
        self.session['name'] = "Nick"    # 设置 Session 方法函数



settings = {
    'template_path':'views',
    'static_path':'statics',
    'cookie_secret':'suoning..................',
}

application = tornado.web.Application([
    (r'/index',IndexHandler),
], **settings)


if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()