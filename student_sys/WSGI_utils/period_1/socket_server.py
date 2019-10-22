"""
代码需要在 Python 3
功能：该文件充当socket服务器、浏览器为客户端
"""
import socket

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
body = '<h1> 我是 HTTP Response HTTP Response HTTP Response<h1>'  # 响应体数据
response_params = [
    'HTTP/1.0 200 OK',
    'Date: Sat, 10 jun 2017 01:01:01 GMT',
    'Content-Type: text/html; charset=utf-8',
    'Content-Length: {}\r\n'.format(len(body)),
    body,
]
response = '\r\n'.join(response_params)  # 返回的HTTP数据要求


def handle_connection(conn, addr):
    """ 处理链接 """
    request = b""  # 网络数据只能是byte型的
    # 判断有没有发送HTTP请求、该过层就是点击打印出的url、HTTP请求有浏览器完成（GET请求）
    # 如没有、接受数据
    while EOL1 not in request and EOL2 not in request:
        request += conn.recv(1024)  # 接受数据
    print(request)  # 打印出请求数据
    conn.send(response.encode())  # 以HTTP格式的数据回复浏览器(客户端) #response 转为bytes 后传输
    conn.close()  # 关闭连接


def main():
    # socket.AF_INET 用于服务器与服务器之间的网络通信
    # socket.SOCK_STREAM 用于基于TCP 的流式socket通信
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 实例化socket
    # 设置棕口可复用，保证我们每次按Ctrl + C组合键之后，快这主启
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('127.0.0.1', 8080))  # 绑定ip 与port
    serversocket.listen(10)  # 监听 设置backlog-socket 连接最大排队数量
    print('http://127.0.0.1:8080')  # 控制台带引url

    try:
        while True:
            conn, address = serversocket.accept()  # 等待客户端建立连接
            handle_connection(conn, address)  # 处理客户端请求
    finally:
        serversocket.close()  # 关闭服务


if __name__ == '__main__':
    main()
