"""
env: python3.6
author: Feo
requirement:
    编写一个服务端http程序，在客户端发起request请求时将网页按照http响应格式发送给浏览器展示
    网页内容作为响应体
    * 注意协调响应格式
    * 对请求做一定的解析判断
      如果请求内容是  '/'   则发送这个网页
                      其他  则用404响应
"""
from socket import *


def handle(connfd):
    # http请求
    request = connfd.recv(4096).decode()
    if not request:
        return
    # 从http请求中提取请求内容
    # print(request)
    # request_line = request.split('\n')[0]
    info = request.split(' ')[1]
    # 根据请求内容组织响应
    if info == '/':
        with open('httpserver1.0/index.html') as f:
            response_body = f.read()
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type:text/html\r\n"
        response += "\r\n"
        response += "%s" % response_body
    else:
        response = "HTTP/1.1 404 Not Found\r\n"
        response += "Content-Type:text/html;charset=UTF-8\r\n"
        response += "\r\n"
        response += "sorry,请求失败"
    connfd.send(response.encode())  # 发送响应
    connfd.close()


def main(addr):
    # http使用tcp传输
    sockfd = socket()
    # 设置端口立即重用
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # 绑定客户端地址
    sockfd.bind(addr)
    sockfd.listen(3)
    print("Listen the port...")
    while True:
        try:
            # 等待浏览器连接
            connfd, addr = sockfd.accept()
            print("Connect From:", addr)
        except KeyboardInterrupt:
            break
        else:
            handle(connfd)  # 处理浏览器请求

    sockfd.close()


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 8080
    addr = (HOST, PORT)
    main(addr)
