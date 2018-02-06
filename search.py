import socket,sys,SocketServer,utils,cloud,os,timeit,pickle,time

class EchoRequestHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        print self.client_address, 'connected!'
        self.request.send('hi ' + str(self.client_address) + '\n')

    def search(self):
        encfm=['pl_100004encfm.pickle','pl_1000004encfm.pickle','pl_10000004encfm.pickle']
        tokens=['tokenpl_10000004_512.pickle','tokenpl_10000004_256.pickle','tokenpl_10000004_128.pickle','tokenpl_10000004_64.pickle']
        #tokens=['tokenpl_100000026_4096.pickle','tokenpl_100000026_1024.pickle']
        key=utils.loadSinglePickle("key.pickle")
        tokd=utils.loadSinglePickle("token.pickle") 
        path=""
        directory = os.listdir('.')  
        for i in tokens:
            tokd=utils.loadSinglePickle(i)
            for f in encfm:
                for ind in tokd:
                    for j in tokd[ind]:
                        print(i,f)
                        #code='res=cloud.search("{}","{}")'.format(f,j)
                        #t = timeit.Timer(stmt=code,setup='from __main__ import utils,cloud')
                        #print ('%f'%float(t.timeit(10/10)))
                        t0 = time.time()
                        res=cloud.search(f,j)
                        t1 = time.time()
                        print('%f',float(t1-t0))
                        with open('res'+i+'_'+f,'wb') as fh:
                            pickle.dump([res],fh,protocol=2)
                    
      #  for i in tokd:
      #      for j in tokd[i]:
      #          tok_file=i+"encfm.pickle"
      #          print("in cloud:"+tok_file)
      #          res=cloud.search(tok_file,j)
      #          print([utils.decryptbox(x,key) for x in res])
        
    def handle(self):
        print("handle")
        self.search()
    
    def finish(self):
        print self.client_address, 'disconnected!'
        #self.request.send('bye ' + str(self.client_address) + '\n')

if __name__=='__main__':
        server = SocketServer.ThreadingTCPServer(('localhost', 60000), EchoRequestHandler)
        server.serve_forever()
