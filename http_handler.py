import threading
import os
import useful
import socket


class TCP_HTTP_HANDLER(threading.Thread):

    def __init__(self, s, conf, preload):
        super(TCP_HTTP_HANDLER, self).__init__()
        self.s = s
        self.PRELOAD = preload
        self.parseCfg(conf)
        self.SETTINGS = SETTINGS
        self.STATUS = STATUS
        self.MIME = MIME
        self.PUBLIC_DIRECTORY = LOCATION["FILES_LOCATION"]
        self.PUBLIC_DIRECTORY_LENGTH = len(self.PUBLIC_DIRECTORY)
        self.ERROR_DIRECTORY = LOCATION["ERROR_LOCATION"]
        self.ERROR_FILES = ERROR_FILES
        self.MESS = MESSAGES
        self.processRequest()

    def parseCfg(self, config):
        try:
            for section, data in config.items():
                globals()[section.upper()] = data
        except ValueError as e:
            useful.error("Configs loading error.", e)

    def tsend(self, string):
        s = self.s
        try:
            return s.sendall(string)
        except (socket.error, AttributeError) as msg:
            useful.error("tsend filed.", msg)
            return False

    def urecv(self, string):
        s = self.s
        data = ""
        rest = ""
        while str(data).find(string) == -1:
            try:
                rest = str(s.recv(1))
                if len(rest) == 0:
                    raise Exception("Bad request.")
            except (socket.error, AttributeError) as msg:
                useful.error("urecv filed.", msg)
                return False
            data += rest
        return str(data)

    def processRequest(self):
        data = ""
        verb = ""
        path = ""
        ver = ""
        try:
            data = self.urecv("\r\n\r\n").splitlines()
            verb, path, ver = data[0].split(" ")
            print data[0]
        except Exception as _:
            self.throwHTTPError("400")
            return

        # <SECURITY>
        if ".." in path or not path.startswith("/"):
            self.throwHTTPError("403")
            return
        # </SECURITY>

        if path == "/":
            path = self.PUBLIC_DIRECTORY + "/index.html"
        else:
            path = self.PUBLIC_DIRECTORY + path
        if not os.path.isfile(path):
            self.throwHTTPError("404")
            return
            
        ext = self.getExt(path)
        file = self.getFile(path)

        # <SECURITY>
        if file == None:
            self.throwHTTPError("500")
            return
        # </SECURITY>
        if self.SETTINGS["PRELOAD"] == "ON" and path[self.PUBLIC_DIRECTORY_LENGTH:] in self.PRELOAD.keys(): #
            file = self.PRELOAD[path[self.PUBLIC_DIRECTORY_LENGTH:]]
            self.sendResponse(file, ext)
            self.close()
            return
        self.sendResponse(file, ext)
        self.close()

    def close(self):
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()

    def getFile(self, path):
        try:
            with open(path) as f:
                data = f.read()
            return data
        except Exception as msg:
            useful.error("Unable to get file.", msg)
            return

    def getExt(self, path):
        _, ext = os.path.splitext(path)
        return ext.lower()

    def getTextStatus(self, status="200"):
        text = self.STATUS.get(status, "OK")
        return text

    def getMime(self, file_name=""):
        _, ext = os.path.split(file_name)
        mime = self.MIME.get(ext, "application/binary")
        return mime

    def sendResponse(self, data, ext=".html", status="200"):  # TODO json
        status_text = self.getTextStatus(status)
        if data is None:
            data = self.MESS["CRITICAL"]
            length = len(data)
            status = "500"
            status_text = self.getTextStatus(status)
        else:
            length = len(data)
        response = "HTTP/1.1 {} {}\r\nContent-Type: {}\r\nContent-Length: {}\r\n\r\n{}".format(
            status, status_text, self.getMime(ext), length, data)
        self.tsend(response)

    def throwHTTPError(self, code="500"):
        code = str(code)
        path = "{}/{}".format(self.ERROR_DIRECTORY, self.ERROR_FILES[code])
        data = self.getFile(path)
        self.sendResponse(data, status=code)
