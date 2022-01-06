import socket, threading, time, json

def main():
    server = Server("0.0.0.0", 80)
    server.verbose = True
    while True:
        try:
            if (server != None):
                server.Run()
        except Exception as error:
            print(error)
            if (server != None):
                server.Stop()
            time.sleep(1)

class Server:
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
            print("Stopping Server")
        self.running = False
        if (self.thread) != None:
            self.thread.join()
            self.thread.close()
            self.thread = None

    def Reconnect(self):
        if (self.verbose == True):
            print("Reconnecting Server")
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, 1000)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, 1000)
            self.socket.bind(("0.0.0.0", 10000))
            self.socket.listen(1)
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
                client, remote = self.socket.accept()
                print(remote)
                if (client != None):
                    request = client.recv(4096).decode()
                    if (self.verbose == True):
                        print(request)
                    data = json.dumps({"message": "Hello From Python!"})
                    response = "HTTP/1.1 200 OK\r\n" \
                             + "Content-Type: application/json\r\n" \
                             + "Content-Length: " + str(len(data)) + "\r\n" \
                             + "\r\n" + data + "\r\n"
                    if (self.verbose == True):
                        print(response)
                    client.send(response.encode())
                    client.close()
                    client = None
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
