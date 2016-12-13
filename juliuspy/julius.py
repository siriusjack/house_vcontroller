import subprocess
import socket


class JuliusServer():
    def __init__(self):
        self.__pid = None

    def start(self):
        if self.__pid is None:
            p = subprocess.Popen(["/bin/bash start-julius.sh"], stdout=subprocess.PIPE, shell=True)
            self.__pid = int(p.stdout.read())
            p.kill()

    def stop(self):
        subprocess.call(["kill " + str(self.__pid)], shell=True)
        self.__pid = None


class Julius():
    def __init__(self, host, port, bufsize=8192):
        self.__server = JuliusServer()
        self.__host = host
        self.__port = port
        self.__bufsize = bufsize
        self.__file = None
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.__server.start()
        self.__socket.connect((self.__host, self.__port))
        self.__file = self.__socket.makefile('')

    def disconenct(self):
        self.__socket.close()
        self.__server.stop()

    def get_stream(self):
        def generator():
            while True:
                if self.__file is not None:
                    yield self.__file.readline()
        return generator()