"""
http服务端主程序
env: python3.6
author: Feo
"""
from socket import *
from threading import Thread
from config import *
import re, json


# 与后端应用交互
def connect_frame(env):
    '''
    将请求发送给WebFrame
    从WebFrame接收反馈数据
    :param env:
    :return:
    '''
    s = socket()
    try:
        s.connect((frame_ip, frame_port))
    except Exception as e:
        print(e)
        return
        # 发送json请求
    data = json.dumps(env)
    s.send(data.encode())
    # 获取返回数据(json格式)
    data = s.recv(1024 * 1024 * 10).decode()
    if data:
        try:
            result = json.loads(data)  # 返回字典
        except:
            pass
        return result


class HTTPServer:
    def __init__(self):
        self.address = (HOST, PORT)
        self.create_socket()
        self.bind()

    # 创建套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)

    # 绑定地址
    def bind(self):
        # 有些属性可以在调用函数时再生产
        self.host = HOST
        self.port = PORT
        self.sockfd.bind(self.address)

    # 处理具体的浏览器请求
    def handle(self, connfd):
        request = connfd.recv(4096).decode()
        pattern = r'(?P<method>[A-Z]+)\s+(?P<info>/\S*)'
        try:
            env = re.match(pattern, request).groupdict()
        except:
            connfd.close()
            return
        else:
            # 与webframe交互(数据字典/None)
            data = connect_frame(env)
            # print(data)
            if data:
                self.response(connfd, data)

    # 组织响应格式
    def response(self, connfd, data):
        # data-->{'status':'200','data':'OK'}
        if data['status'] == '200':
            res = "HTTP/1.1 200 OK\r\n"
            res += "Content-Type:text/html;charset=UTF-8\t\n"
            res += "\r\n"
            res += data['data']
        elif data['status'] == '404':
            res = "HTTP/1.1 404 Not Found\r\n"
            res += "Content-Type:text/html;charset=UTF-8\t\n"
            res += "\r\n"
            res += data['data']
        connfd.send(res.encode())  # 响应给浏览器

    def server_forever(self):
        self.sockfd.listen(3)
        print("Listen the port %d..." % self.port)
        while True:
            connfd, addr = self.sockfd.accept()
            print("Connect from", addr)
            t = Thread(target=self.handle, args=(connfd,))
            t.setDaemon(True)
            t.start()


if __name__ == '__main__':
    httpd = HTTPServer()
    httpd.server_forever()  # 启动服务
