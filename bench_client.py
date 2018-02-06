#!/usr/bin/env python
import sys,utils,timeit
import nacl.secret                                                                                                          
import nacl.utils,pickle
import fm,socket,os,utils,random,argparse


HOST, PORT = "localhost", 50000


def getConn():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    return sock    
    
    #with open('key.pickle', 'wb') as handle:
    #  pickle.dump(key, handle, protocol=2)
def createData():
    dsize=[10**2,10**3,10**4,10**5,10**6]
    vc=[2,4,26]
    #Create datasets with variable size and vocabulary
    for s in dsize:
        for v in vc:
            filename="./data/pl_"+str(s)+str(v)
            utils.createData(filename,s,v)
    for s in dsize:
        for v in vc:
            fc,lc,sa,digc,digv=fm.build_FM(filename)
            #code='fm.encrypt_FM(fc,lc,sa,key,digc,digv,nonce,"pl_"+str(s)+str(v))'
            fm.encrypt_FM(fc,lc,sa,key,digc,digv,nonce,"pl_"+str(s)+str(v))
            #t = timeit.Timer(stmt=code,setup='from __main__ import fm,fc,lc,digc,digv,sa,key,nonce,s,v,vc')
            #print("pl_"+str(s)+str(v))
            #print ('%f'%float(t.timeit(10/10)))

    #token(sys.argv[1],'key.pickle')

def parseRealData(filename,window,chars,key,nonce):
    fc,lc,sa,digc,digv,isize=fm.build_FM(filename,window,chars)
    #print fc,lc
    #fm.encrypt_FM(fc,lc,sa,key,digc,digv,nonce,"pl_"+filename,isize)
    fm.bucket_encrypt_FM(fc,lc,sa,key,digc,digv,nonce,"pl_"+filename,isize,window)
    return


#Send plaintext datasets
#path="./data/"
#directory = os.listdir(path)
#for filename in directory:
#        print(filename)
#        sock=getConn()
#
#
#        sock.sendall(filename+"\n")
#
#            # Receive data from the server and shut down
#        received = sock.recv(1024)
#        print "Received: {}".format(received)
#        data = open(os.path.join(path, filename), 'rb').read()
#        sock.send(data)
#        #received = sock.recv(1024)
#        #print "Received: {}".format(received)
#  
#        sock.close()

##Send encrypted FM index
def sendFM():
    path="./pickles/"
    directory = os.listdir(path)
    for filename in directory:
            print(filename)
            sock=getConn()


            sock.sendall(filename+"\n")
            received = sock.recv(1024)
            print "Received: {}".format(received)
            data = open(os.path.join(path, filename), 'rb').read()
            sock.send(data)
      
            sock.close()


def createTokens():
    keypath=('pickles/key.pickle')
    path="./data/"
    directory = os.listdir(path)
    tok={}
    print('create tokens..')
    t=[2**4,2**5,2**6,2**7,2**8,2**9,2**10,2**12]
    files=['pl_100000026']
    for filename in files:
        for i in t:
            #code='etok=utils.token("{}","{}","{}")'.format(filename, keypath, str(i))
            etok=utils.token(filename, keypath, str(i))
            #t = timeit.Timer(stmt=code,setup='from __main__ import utils')
            #print(filename+'_'+str(i+1)+'.pickle')
            #print ('%f'%float(t.timeit(10/10)))
            sock=getConn()
            sock.sendall('token'+filename+'_'+str(i)+'.pickle'+"\n")
            received = sock.recv(1024)
            print "Received: {}".format(received)
            data = open('./pickles/token'+filename+'_'+str(i)+'.pickle', 'rb').read()
            sock.sendall(data)

            sock.close()


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', help='Path of file to encrypt')
    parser.add_argument('--window', '-w', help='window size of the bucket')
    parser.add_argument('--chars', '-c', help='number of chars')
    args = parser.parse_args()

        
    #Same key used for different files!
    key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
    nonce =nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    utils.writePickle('./pickles/key.pickle',key)
    parseRealData(args.filename,int(args.window),int(args.chars))
    #createData()
    #sendFM()
    #createTokens()




