import nacl.secret
import nacl.utils
import sys,string
from collections import Counter
from pyblake2 import blake2b
import struct,random,os,errno,pickle
def xor_strings(xs, ys):      
    return hex(int(xs, 16) ^ int(ys, 16))
    #return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))


def prf(input,key):#blake2
    h = blake2b(key, digest_size=16) 
    h.update(input)
    return h.hexdigest()


def encryptbox(message,key,nonce):#salsa20+Poly1305
    box = nacl.secret.SecretBox(key)
    encrypted = box.encrypt(message, nonce)
    return encrypted
def decryptbox(message,key):
    box = nacl.secret.SecretBox(key)
    decrypted = box.decrypt(ciphertext=message)
    return decrypted
def readfile(sd):
    s=""
    with open(sd,'r') as myfile:
         s =myfile.read()
    return s.rstrip('\n')

def createData(sd,N,v):
    if not os.path.exists(os.path.dirname(sd)):
        os.makedirs(os.path.dirname(sd))
    #os.makedirs(os.path.dirname(sd), exist_ok=True) 
    with open(sd, "wb") as sink:
    #sink.write(''.join(random.choice('ABCD') for _ in xrange(int(N))))
    #sink.write(''.join(random.choice('ABCDEFGHIJKLMNOP') for _ in xrange(int(N))))
        if v==26:
            sink.write(''.join(random.choice(string.ascii_uppercase) for _ in xrange(int(N))))
            sink.write('$')
        elif v==4:
            sink.write(''.join(random.choice('ACGT') for _ in xrange(int(N))))
            sink.write('$')
        elif v==2:
            sink.write(''.join(random.choice('01') for _ in xrange(int(N))))
            sink.write('$')

    return


def writePickle(sd,data):
    if not os.path.exists(os.path.dirname(sd)):
        os.makedirs(os.path.dirname(sd))
    with open(sd, 'wb') as handle:
        pickle.dump(data, handle, protocol=2)
    return

def loadIndex(name):
    with open(name,'rb') as handle:
        efm,llset=pickle.load(handle)
    return efm,llset

def loadSinglePickle(name):
    with open(name,'rb') as handle:
        tok=pickle.load(handle)
    return tok 
def token(fp,kfp,tks):
    path='./data/'
    a=[]
    etok=[]
    #read key from pickle file
    with open(kfp,'rb') as f:
        key=pickle.load(f)
    #read 3 chars from the file    
    with open(path+fp,'rb') as fh:
        fh.seek(23)
        for i in range(int(tks)):
            a.append(fh.read(1))   
    #encrypt token
    for i in range(len(a)):
        etok.append(prf(str(a[i]),b'pseudorandom'))
    #print(a)
    #print(etok)
    #with open('./pickles/token.pickle', 'wb') as handle:
    #  pickle.dump(etok, handle, protocol=2)
    return etok

