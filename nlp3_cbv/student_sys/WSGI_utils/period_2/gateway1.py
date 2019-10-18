import os
import sys

"""
问题：标准输出流与标准输入流的作用
sys.stdout.write(data)
sys.stdout.flush()

改代码、调用及结构都值得深入研究！
"""

def simple_app(environ, start_response):
    """Simplest possible application object"""
    print(environ, start_response)
    # print(start_response)
    print('\n\r')
    status = '200 OK'  # 状态码、标志
    response_headers = [('Content-type', 'text/html')]  # 响应头
    start_response(status, response_headers)  # 此处调用了start_response函数
    return ['Hello Bruce!\n']

# 这个函数的逻辑应该注意
def run_with_cgi(application):
    environ = dict(os.environ.items())  # 获得系统的各种信息、以字典形式返回
    # 向字典中添加元素
    environ['wsgi.input'] = sys.stdin
    environ['wsgi.errors'] = sys.stderr
    environ['wsgi.version'] = (1, 0)
    environ['wsgi.multithread'] = False
    environ['wsgi.multiprocess'] = True
    environ['wsgi.run_once'] = True

    # 判断使用的是https协议还是http协议
    if environ.get('HTTPS', 'off') in ('on', '1'):
        environ['wsgi.url_scheme'] = 'https'
    else:
        environ['wsgi.url_scheme'] = 'http'

    headers_set = []
    headers_sent = []

    # 内部函数
    def write(data):
        # out = sys.stdout.buffer  # 输出流缓存

        # 如果没有发送了header、则抛出AssertionError异常
        if not headers_set:
            raise AssertionError("write() before start_response()")  # 在发送响应之前先写入

        elif not headers_sent:
            # 在输出第一行数据之前、想发送响应头
            # Before the first output, send the stored headers
            status, response_headers = headers_sent[:] = headers_set
            sys.stdout.write('Status: %s\r\n' % status)  # 写状态码
            for header in response_headers:
                sys.stdout.write('%s: %s\r\n' % header)  # 写响应头
            sys.stdout.write('\r\n')

        sys.stdout.write(data)
        sys.stdout.flush()

    # 内部函数
    def start_response(status, response_headers, exc_info=None):
        if exc_info:
            try:
                if headers_sent:
                    # 如果已经发送了header, 则重新抛出原始异常信息
                    # Re-raise original exception if headers sent
                    raise (exc_info[0], exc_info[1], exc_info[2])
            finally:
                exc_info = None     # avoid dangling circular ref  避免循环引用
        elif headers_set:
            raise AssertionError("Headers already set!")

        headers_set[:] = [status, response_headers]
        return write

    # 注意：定义的函数内部函数在函数内部调用
    result = application(environ, start_response)
    # print(result)
    # print(headers_set)
    # print(headers_sent)
    try:
        for data in result:
            if data:    # don't send headers until body appears 如采没有body 数据，则不发送header
                write(data)
        if not headers_sent:
            write('')   # send headers now if body was empty  如果body 为空，就发送数据header
    finally:
        if hasattr(result, 'close'):
            result.close()


if __name__ == '__main__':
    # run_with_cgi(application)
    run_with_cgi(simple_app)
