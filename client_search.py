#!/usr/bin/env python
import sys,utils
import nacl.secret                                                                                                          
import nacl.utils,pickle
import fm,socket,os,utils


HOST, PORT = "localhost", 60000


def getConn():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    return sock    
if __name__=='__main__':
    sock=getConn()
