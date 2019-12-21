"""
web框架
env: python3.6
author: Feo
"""
from threading import Thread
from settings import *
from socket import *
import json
from urls import *


class Application:
    def __init__(self):
        self.address = (HOST, PORT)
        self.create_socket()
        self.bind()

    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)

    def bind(self):
        self.host = HOST
        self.port = PORT
        self.sockfd.bind(self.address)

    def start(self):
        self.sockfd.listen(3)
        print("Running web frame %d..." % self.port)
        while True:
            connfd, addr = self.sockfd.accept()
            print("Connect from", addr)
            t = Thread(target=self.handle, args=(connfd,))
            t.setDaemon(True)
            t.start()

    def handle(self, connfd):
        request = connfd.recv(4096).decode()
        request = json.loads(request)  # 请求字典
        # request->{'method':'GET','info':'xxx'}
        # print(request)
        if not request:
            connfd.close()
            return
        # 解析请求，提取请求内容
        # 根据请求内容分为两类
        if request['method'] == 'GET':
            if request['info'] == '/' or request['info'][-5:] == '.html':
                response = self.get_html(request['info'])
            else:
                response = self.get_data(request['info'])
        elif request['method'] == 'POST':
            pass
        # 将数据传给httpserver
        # reponse->{'status': '200', 'data': 'xxx'}
        response = json.dumps(response)
        connfd.send(response.encode())
        connfd.close()

    # 网页处理
    def get_html(self, info):
        if info == '/':
            filename = DIR + '/index.html'
        else:
            filename = DIR + info
        try:
            with open(filename) as f:
                data = f.read()
        except Exception as e:
            with open(DIR + '/404.html') as fd:
                data = fd.read()
            return {'status': '404', 'data': data}
        else:
            return {'status': '200', 'data': data}

    # 其他处理
    def get_data(self, info):
        for url, func in urls:
            if url == info:
                return {'status': '200', 'data': func()}
        return {'status': '404', 'data': 'Sorry...'}


if __name__ == '__main__':
    app = Application()
    app.start()  # 启动应用
