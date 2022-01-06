import socket, threading, time, json

def main():
    client = Client("localhost", 10000)
    client.verbose = True
    while True:
        try:
            if (client != None):
                client.Run()
        except Exception as error:
            print(error)
            if (client != None):
                client.Stop()
            time.sleep(1)

class Client:
    def __init__(self, Address, Port):
        self.address = Address
        self.port = Port
        self.mtu = 1500
        self.running = False
        self.verbose = False
        self.thread = None
        self.socket = None

    def Run(self):
        if (self.thread == None) or (not self.thread.is_alive()):
            self.running = True
            self.thread = threading.Thread(target = self.Procedure)
            self.thread.start()

    def Stop(self):
        if (self.verbose) == True:
            print("Stopping Client")
        self.running = False
        if (self.thread) != None:
            self.thread.join()
            self.thread.close()
            self.thread = None

    def Reconnect(self):
        if (self.verbose == True):
            print("Reconnecting Client")
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, 1000)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, 1000)
            self.socket.connect((self.address, self.port))
        except Exception as error:
            if (self.verbose == True):
                print(error)
            self.socket = None
            time.sleep(1)

    def Procedure(self):
        while (self.running == True):
            try:
                if (self.socket == None):
                    self.Reconnect()
                    return
                if (self.socket != None):
                    request = "GET / HTTP/1.1\r\n"
                    if (self.verbose == True):
                        print(request)
                    self.socket.send(request.encode())
                    response = self.socket.recv(4096)
                    if (self.verbose == True):
                        print(response.decode())
                    self.socket.close()
                    self.socket = None
            except Exception as error:
                if (self.verbose == True):
                    print(error)
                if (self.socket != None):
                    self.socket.close()
                    self.socket = None
                time.sleep(1)
        if (self.socket != None):
            self.socket.close()
            self.socket = None

if __name__ == "__main__":
    main()
