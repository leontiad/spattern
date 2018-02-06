import socket,sys,SocketServer
from threading import Thread


class EchoRequestHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        print self.client_address, 'connected!'
        self.request.send('hi ' + str(self.client_address) + '\n')

    def getFile(self):
            fle = self.request.makefile('r')
            filename = fle.readline()
            print("Got filename {}\n".format(filename))
            data = 'fnord' # just something to be there for the first comparison
            with open(filename[:-1], 'w') as outfile:
                while data:
                    #data = self.request.recv(1024)
                    data = fle.read()
                    #print('writing {!r} to file ....'.format(data))
                    outfile.write(data)
                    print("Finish {}\n".format(filename))
            print("finish handle")
    def handle(self):
        print("handle")
        self.getFile()
        print("finish_handle")
    
    def finish(self):
        print self.client_address, 'disconnected!'
        #self.request.send('bye ' + str(self.client_address) + '\n')
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
if __name__=='__main__':
        #server = SocketServer.ThreadingTCPServer(('localhost', 50000), EchoRequestHandler)
        server = ThreadedTCPServer(('localhost', 50000), EchoRequestHandler)
        server.serve_forever()
