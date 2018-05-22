import threading
import os
import useful
import socket
from http_handler import *
import load_config
import preload
class TCP_HTTP():
    
    def __init__(self, host, port, slots=5):
        self.s = self.openTCP(host, port, slots)
        self.cfg = load_config.loadConfigFiles()
        preload_list = preload.loadPreloadLits()
        self.preload = preload.getPreloadFiles(preload_list)
        self.run()

    def openTCP(self, host, port, slots):
        """
        Opens TCP server.
        Usage:
            None.
        """
        addr = (host, port)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(addr)
            s.listen(slots)
            return s
        except socket.error as msg:
            useful.error("TCP socket filed.", msg)
            return False
        
    def run(self, s=None):
        if s is None and self.s:
            s = self.s
        else:
            useful.error("TCP socket filed")
        try:
            while True:
                conn, addr = s.accept()
                useful.alert("New connection established: {}".format(addr))
                th = TCP_HTTP_HANDLER(conn, self.cfg, self.preload)
                th.deamon = False
                th.start()
        except (socket.error, AttributeError) as msg:
            useful.error("Accept filed.", msg)
            return False    
