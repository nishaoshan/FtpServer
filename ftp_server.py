"""
author : Nishaoshan
email : 790016602@qq.com
time : 2020-6-21
env : Python3.6
socket,os,Thread,time,文件服务，器服务器端，查看，下载，上传
"""
from socket import *
import os
from threading import Thread
from time import sleep


class Ftp_server:
    def __init__(self, host="0.0.0.0", port=9998):
        self.host = host
        self.port = port
        self.sock = socket()
        self.sock.bind((self.host, self.port))

    def start(self):
        self.sock.listen(3)
        while True:
            try:
                connfd, addr = self.sock.accept()
            except KeyboardInterrupt:
                return
            print("connect from ", addr)
            t = Function(connfd)
            t.daemon = True
            t.start()


class Function(Thread):
    def __init__(self, connfd, path="/home/tarena/2004/month01/day04/"):
        super().__init__()
        self.connfd = connfd
        self.dir = path

    def run(self):
        while True:
            request = self.connfd.recv(1024).decode()
            if request == "q":
                self.connfd.close()
                return
            elif request == "c":
                file_list = os.listdir(self.dir)
                if file_list:
                    self.connfd.send(b"ok")
                    sleep(0.1)
                    self.connfd.send("\n".join(file_list).encode())
                else:
                    self.connfd.send(b"fail")
            elif request.split(" ")[0] == "d":
                filename = request.split(" ")[1]
                try:
                    f = open(self.dir + filename, "rb")
                except:
                    print("文件不存在")
                    self.connfd.send(b"fail")
                else:
                    self.connfd.send(b"ok")
                    sleep(0.1)
                    while True:
                        data = f.read(1024)
                        if not data:
                            sleep(0.1)
                            self.connfd.send(b"over")
                        self.connfd.send(data)

            elif request.split(" ")[0] == "u":
                if request.split(" ")[1] in os.listdir(self.dir):
                    self.connfd.send(b"cover")
                    data = self.connfd.recv(1024)
                    if data == b"y":
                        f = open(self.dir + request.split(" ")[1], "wb")
                        while True:
                            data = self.connfd.recv(1024)
                            if data == b"over":
                                break
                            f.write(data)
                        f.close()
                    else:
                        return

                else:
                    self.connfd.send(b"ok")
                    f = open(self.dir + request.split(" ")[1], "wb")
                    while True:
                        data = self.connfd.recv(1024)
                        if data == b"over":
                            break
                        f.write(data)
                    f.close()


if __name__ == '__main__':
    Ftp_server().start()
