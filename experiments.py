import bench_client as b
import sys,timeit                                                                                                     
import nacl.secret                                                                                                          
import nacl.utils,pickle                                                                                                    
import fm,os,utils,random,argparse 

ssize=[11]
window=[4]
fname='data/ex_enron.txt'
key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)                                                                 
nonce =nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)                                                              
utils.writePickle('./pickles/key.pickle',key)                                                                           
for size in ssize:
    for win in window:
        b.parseRealData(fname,win,size,key,nonce) 

