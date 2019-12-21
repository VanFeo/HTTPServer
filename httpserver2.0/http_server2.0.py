"""
http_server2.0
"""
import os
from socket import *
from select import select


class HTTPServer:
    def __init__(self, host='0.0.0.0', port=8080, dir=None):
        self.Host = host
        self.Port = port
        self.address = (host, port)
        self.dir = dir
        # 直接创建套接字
        self.create_socket()

    # 创建套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sockfd.bind(self.address)

    # 启动服务
    def serve_forever(self):
        self.sockfd.listen(3)
        print("Listen the port %d..." % self.Port)
        # IO多路复用
        self.rlist = [self.sockfd]
        self.wlist = []
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, [])
            for r in rs:
                if r == self.sockfd:
                    # 浏览器连接
                    connfd, addr = r.accept()
                    print("Connect from", addr)
                    self.rlist.append(connfd)
                else:
                    # 处理具体请求
                    self.handle(r)

    def handle(self, c):
        request = c.recv(1024).decode()
        # print(request)
        if not request:
            self.rlist.remove(c)
            c.close()
            return
        # 解析请求，提取请求内容
        request_line = request.split('\n')[0]
        info = request_line.split(' ')[1]
        print(c.getpeername(), ':', info)  # 获取客户端地址
        # 根据请求内容分为两类
        if info == '/' or info[-5:] == '.html':
            self.get_html(c, info)
        else:
            self.get_data(c, info)
        c.close()
        self.rlist.remove(c)

    def get_html(self, c, info):
        if info == '/':
            filename = self.dir + '/index.html'
        else:
            filename = self.dir + info
        try:
            with open(filename) as f:
                data = f.read()
        except Exception:
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type:text/html;charset=UTF-8\r\n"
            response += '\r\n'
            response += "<h1>网页不存在</h1>"
        else:
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += '\r\n'
            response += data
        finally:
            # 将响应发送给浏览器
            c.send(response.encode())

    def get_data(self, c, info):
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type:text/html\r\n"
        response += '\r\n'
        response += "<h1>Waiting for httpserver3.0</h1>"
        c.send(response.encode())


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 8080
    DIR = 'httpserver2.0/static'
    httpd = HTTPServer(HOST, PORT, DIR)
    httpd.serve_forever()  # 启动服务
