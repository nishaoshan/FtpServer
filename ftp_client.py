"""
author : Nishaoshan
email : 790016602@qq.com
time : 2020-6-21
env : Python3.6
socket,os,Thread,time,文件服务，器服务器端，查看，下载，上传
"""
from socket import *
from time import sleep


class FtpClient:
    def __init__(self, host="127.0.0.1", port=9998):
        self.host = host
        self.port = port
        self.sock = socket()
        self.sock.connect((self.host, self.port))

    def main(self):
        while True:
            print("------c------")
            print("-d filename--")
            print("-u filename--")
            print("------q------")

            order = input("请输入指令:")
            filename = order.split(" ")[-1]
            if order == "c":
                self.c()
            elif order.split(" ")[0] == "d":
                self.d(filename)
            elif order.split(" ")[0] == "u":
                self.u(filename)
            elif order.split(" ")[0] == "q":
                self.q()
                break
            else:
                print("输入有误，请重新输入")

    def q(self):
        self.sock.send(b"q")
        self.sock.close()

    def c(self):
        self.sock.send(b"c")
        data = self.sock.recv(1024).decode()
        if data == "ok":
            data = self.sock.recv(1024).decode()
            print(data)
        else:
            print("文件库为空")

    def u(self, filename):
        try:
            f = open(filename, "rb")
        except:
            print("文件不存在")
        else:
            self.sock.send(f"u {filename}".encode())
            data = self.sock.recv(1024)
            if data == b"ok":
                while True:
                    data = f.read(1024)
                    if not data:
                        sleep(0.1)
                        self.sock.send(b"over")
                    self.sock.send(data)
            elif data == b"cover":
                while True:
                    res = input("文件已存在，是否要覆盖(y/n)")
                    if res == "y":
                        self.sock.send(b"y")
                        sleep(0.1)
                        while True:
                            data = f.read(1024)
                            if not data:
                                sleep(0.1)
                                self.sock.send(b"over")
                                return
                            self.sock.send(data)
                    elif res == "n":
                        self.sock.send(b"n")
                        return
                    else:
                        print("输入有误请重新输入")

    def d(self, filename):
        self.sock.send(f"d {filename}".encode())
        data = self.sock.recv(1024).decode()
        if data == "ok":
            f = open(f"./{filename}", "wb")
            while True:
                data = self.sock.recv(1024)
                if data == b"over":
                    break
                f.write(data)
            f.close()
        else:
            print("文件不存在，请重新输入")


if __name__ == '__main__':
    FtpClient().main()
