import os
import sys

def simple_app(environ, start_response):
    """Simplest possible application object"""
    print(environ, start_response)
    print('\n\r')
    status = '200 OK'  # 状态码、标志
    response_headers = [('Content-type', 'text/html')]  # 响应头
    start_response(status, response_headers)
    return ['Hello simple_app world!\n']


class AppClass(object):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]

    def __call__(self, environ, start_response):
        print(environ, start_response)
        start_response(self.status, self.response_headers)
        return ['Hello AppClass.__call__\n']

def wsgi_to_bytes(s):
    return s.encode()

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

    def write(data):
        if not headers_set:
            raise AssertionError("write() before start_response()")

        elif not headers_sent:
            # Before the first output, send the stored headers
            status, response_headers = headers_sent[:] = headers_set
            sys.stdout.write('Status: %s\r\n' % status)
            for header in response_headers:
                sys.stdout.write('%s: %s\r\n' % header)
            sys.stdout.write('\r\n')

        sys.stdout.write(data)
        sys.stdout.flush()

    def start_response(status, response_headers, exc_info=None):
        if exc_info:
            try:
                if headers_sent:
                    # Re-raise original exception if headers sent
                    # raise exc_info[0], exc_info[1], exc_info[2]
                    raise exc_info[0]
            finally:
                exc_info = None     # avoid dangling circular ref
        elif headers_set:
            raise AssertionError("Headers already set!")

        headers_set[:] = [status, response_headers]
        return write

    result = application(environ, start_response)
    try:
        for data in result:
            if data:    # don't send headers until body appears
                write(data)
        if not headers_sent:
            write('')   # send headers now if body was empty
    finally:
        if hasattr(result, 'close'):
            result.close()

application = AppClass()

if __name__ == '__main__':
    run_with_cgi(simple_app)
    # run_with_cgi(application)
