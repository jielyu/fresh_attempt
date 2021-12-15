#encoding: utf-8

import os
import sys
import socket
import select

"""
本代码的socket事件循环参考clowwindy的ss实现
"""


class SelectLoop:
    """使用select多路复用socket实现高并发"""

    POLL_READ = 0x01    # 读事件监听模式
    POLL_WRITE = 0x04   # 写事件监听模式
    POLL_ERR = 0x08     # 错误时间监听模式

    def __init__(self) -> None:
        """构造函数"""
        self._read_set = set()  # 监听读事件集合
        self._write_set = set() # 监听写事件集合
        self._err_set = set()   # 监听错误事件集合
        # 将集合存储问词典，便于操作
        self._rwx_map = {self.POLL_READ: self._read_set, 
            self.POLL_WRITE: self._write_set, self.POLL_ERR: self._err_set}

    def poll(self, timeout):
        """查询就绪的socket，没有任何就绪则阻塞
        
        Args:
            timeout: 超时时间，单位：秒

        Returns:
            list, [(fd, modes), ...]: 就绪的socket文件描述符和模式
        
        """
        r, w, x = select.select(self._read_set, self._write_set, self._err_set, timeout)
        fd_mode_list = [(self.POLL_READ, r), (self.POLL_WRITE, w), (self.POLL_ERR, x)]
        ret = {}
        for fd_mode in fd_mode_list:
            for fd in fd_mode[1]:
                if fd not in ret:
                    ret[fd] = fd_mode[0]
                else:
                    ret[fd] |= fd_mode[0]
        return ret.items()

    def register(self, fd, mode):
        """注册一个socket"""
        for m in list(self._rwx_map.keys()):
            if m & mode:
                self._rwx_map[m].add(fd)
        return True

    def unregister(self, fd):
        """剔除一个scoket"""
        for _, v in self._rwx_map.items():
            if fd in v:
                v.remove(fd)
        return True

    def modify(self, fd, mode):
        """修改socket的监听模式"""
        self.unregister(fd)
        self.register(fd, mode)


class EventLoop:
    """事件循环用于将阻塞事件划分为多个部分事件循环分发执行"""

    def __init__(self) -> None:
        """事件循环的构造函数"""
        self._select_loop = SelectLoop()
        # 文件描述符与处理之间的映射 {fd: (f, handler)}
        self._fd_handler_map = {}

    def poll(self, timeout):
        """查询就绪的事件，没有任何就绪则阻塞
        
        Args:
            timeout: 超时事件

        Returns:
            list, [(f, fd, modes)]: 返回socket文件对象，文件描述符以及事件模式

        """
        es = self._select_loop.poll(timeout)
        return [(self._fd_handler_map[fd][0], fd, modes) for fd, modes in es]

    def register(self, f, mode, handler):
        """注册一个socket事件，并指定处理器"""
        fd = f.fileno()
        self._fd_handler_map[fd] = (f, handler)
        self._select_loop.register(fd, mode)
        return True

    def unregister(self, f):
        """剔除一个socket事件"""
        fd = f.fileno()
        del self._fd_handler_map[fd]
        self._select_loop.unregister(fd)
        return True

    def modify(self, f, mode):
        """修改一个socket事件的监听模式"""
        fd = f.fileno()
        self._select_loop.modify(fd, mode)
        return True

    def size(self):
        """查询当前事件循环中的socket个数"""
        return len(self._fd_handler_map)

    def run(self):
        """事件循环的主流程"""
        es = []
        while True:
            print('distribute event ...')
            try:
                es = self.poll(10)
            except Exception as e:
                print(e)
                continue
            print('num events:{}'.format(len(es)))
            for f, fd, mode in es:
                handler = self._fd_handler_map.get(fd, None)
                if handler is not None:
                    handler = handler[1]
                    handler.handle(f, fd, mode)


class SocketHandler:
    """封装Socket处理流程"""

    def __init__(self, ip, port, event_loop) -> None:
        """构造socket处理对象"""
        self._event_loop = event_loop
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((ip, port))
        self.socket.listen(5)
        self.socket.setblocking(False)
        print('start server on {}:{} ...'.format(ip, port))

    def handle(self, sock, fd, mode):
        """响应socket事件的函数"""
        print('mode={}, loop.size()={}'.format(mode, self._event_loop.size()))
        if sock == self.socket:
            conn, addr = sock.accept()
            self._event_loop.register(conn, SelectLoop.POLL_READ, self)
        else:
            if mode & SelectLoop.POLL_READ:
                data = sock.recv(1024)
                print(data)
                if data:
                    sock.send(data.upper())
                else:
                    self._event_loop.unregister(sock)


def test_socket():
    server = socket.socket()
    server.bind(('127.0.0.1', 50051))
    server.listen(5)
    print('start server on 127.0.0.1 listen port 50051 ...')
    while True:
        conn, addr = server.accept()
        print(conn, addr)
        while True:
            data = conn.recv(1024)
            print(data)
            if not data:
                print('recv complete')
                break
            conn.send(data.upper())
    server.close()


def main():
    ip = '127.0.0.1'
    port = 50051
    event_loop = EventLoop()
    handler = SocketHandler(ip, port, event_loop)
    event_loop.register(handler.socket, SelectLoop.POLL_READ|SelectLoop.POLL_ERR, handler)
    event_loop.run()

if __name__ == '__main__':
    main()
