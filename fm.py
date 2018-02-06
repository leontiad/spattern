import bwt
import nacl.secret
import nacl.utils
import sys
from collections import Counter
from pyblake2 import blake2b
from collections import OrderedDict
import pickle
import utils,operator,random

'''Returns a dictionary with keys all the unique characters and the rankings, 
and values their PRF evaluation return digs{char,rank:blake2b()}'''
def precompute(inp):#PRF all the unique characters and rankings.
    data=Counter(inp)
    #print(data)
    digc={}
    digv={}
    #digc['$']=utils.prf(str('$'),b'pseudorandom')
    for i in range(max(data.values())+int(1)):
        digv[i]=utils.prf(str(i),b'pseudorandom')
    for k,v in data.iteritems():
        digc[k]=(utils.prf(str(k),b'pseudorandom'),data[k])
    return digc,digv
#mydict = {'george':16,'amber':19}
#print mydict.keys()[mydict.values().index(16)] 

# search in tuples [i for i, v in enumerate(L) if v[0] == 53]
def encrypt_FM(keys,values,pos,sk,digc,digv,nonce,fname,isize):
    efm=OrderedDict()
    #print keys
    #print values
    #efm = {utils.xor_strings(digc[(keys[i][0])][0],digv[keys[i][1]]):(digc[values[i][0]][0],digv[values[i][1]],utils.encryptbox(str(pos[i]),sk,nonce)) for i in range(len(keys))}
    efm = {utils.xor_strings(digc[(keys[i][0])][0],digv[keys[i][1]]):(digc[values[i][0]][0],digv[values[i][1]],utils.encryptbox(str(pos[i]),sk,nonce),utils.encryptbox(str(i),sk,nonce)) for i in range(len(keys))}
    #llset={v[0]:efm[xor_strings(v[0],digv[i])] for (k,v) in digc.items() for i in range(v[1])}
    
    #llset={prf(c):[(),(),...()]}
    llset={}
    digc.pop('$',None)
    for (k,v) in digc.items():
        for i in range(int(v[1])):
            #vv=efm[utils.xor_strings(v[0],digv[i])]
            vv=utils.xor_strings(v[0],digv[i])
            llset.setdefault(v[0], []).append(vv)
    #print(llset)
    #esa = [utils.encryptbox(str(pos[i]),sk,nonce) for i in pos]
    #print('file='+str(fname)+'size='+str(len(llset)))
    utils.writePickle('./pickles/bucket'+str(fname)+str(isize)+'_encfm.pickle',[efm,llset])
    return
    #with open(str(fname)+'encfm.pickle', 'wb') as handle:
    #    pickle.dump([efm,llset], handle, protocol=2)


def bucket_encrypt_FM(keys,values,pos,sk,digc,digv,nonce,fname,isize,win):
    efm=OrderedDict()
    efm = {utils.xor_strings(utils.prf(keys[i][0],b'pseudorandom'),utils.prf(keys[i][1],b'pseudorandom')):(utils.prf(values[i][0],b'pseudorandom'),utils.prf(values[i][1],b'pseudorandom'),utils.encryptbox(str(pos[i]),sk,nonce),utils.encryptbox(str(i),sk,nonce)) for i in range(len(keys))}
    llset={}
    for (k,v) in digc.items():
        print k,v
        for i in range(int(v[1])):
            #vv=efm[utils.xor_strings(v[0],digv[i])]
            vv=utils.xor_strings(v[0],digv[i])
            llset.setdefault(v[0], []).append(vv)
    utils.writePickle('./pickles/bucket'+str(fname)+'win='+str(win)+'chars='+str(isize)+'_encfm.pickle',[efm,llset])

def dummy(stream):
    c=Counter(stream)
    #store the maximum frequency character
    maxf=max(c.iteritems(), key=operator.itemgetter(1))[0]
    minf=min(c.iteritems(), key=operator.itemgetter(1))[0]
    mv=c[maxf]
    minv=c[minf]
    print('max frequency='+str(mv))
    j=0
    s=""
    for k,x in c.iteritems():
        if k!='$':
            s=s+(mv-x)*k
            j=j+(mv-x)
    s=''.join(random.sample(s,len(s)))
    print len(s)
    rs=random.randint(1, 10)
    #uncomment in case of single char solution
    #stream=s[:rs]+stream+s[rs+1:]
    stream.append(s)
    return stream

#Generate a list of buckets from the original stream
def bucket_stream(s,win):
    L=[]
    for i in range(len(s)-win+1):
        L.append(s[i:i+win])    
    #print L
    return L

def build_FM(fname,window,chars):
    st,isize=utils.readfile(fname,chars)
    print st
    stream=bucket_stream(st,window)
    print stream
    #print stream
    digc=0
    digv=0
    olen=len(stream)
    stream=dummy(stream)
    digc,digv=precompute(stream)
    #b=bwt.bwtViaBwm(stream)
    b,sa,fc = bwt.bwtViaSa(stream,st,window)
    #print 'b='+str(b)
    #print 'sa='+str(sa)
    #print 'fc='+str(fc)
    ranks,tots = bwt.rankBwt(b)
    ra,to = bwt.rankBwt(fc)
    fc=zip(fc,ra)
    lc=zip(b,ranks)
    #fc=[x[0] for x in bwt.bwm(stream)]
    #fc= ''.join(fc)
    #fc= zip(fc,ranks)
    #print ("FC="+str(fc)+"\nLC="+str(lc)+"\nSA="+str(sa)+"\ndigc="+str(digc)+"\ndigv="+str(digv))
    return fc,lc,sa,digc,digv,isize


def token(fp,kfp,tks):
    a=[]
    etok=[]
    #read key from pickle file
    with open(kfp,'rb') as f:
        key=pickle.load(f)
    #read 3 chars from the file
    with open(fp,'rb') as fh:
        fh.seek(23)
        for i in range(tks):
            a.append(fh.read(1))
    #encrypt token
    for i in range(len(a)):
        etok.append(utils.prf(str(a[i]),b'pseudorandom'))
    #print(a)
    #print(etok)
    with open('token.pickle', 'wb') as handle:
      pickle.dump(etok, handle, protocol=2)
    return

def main():
    key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
    nonce =nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    fname= sys.argv[1]
    N =sys.argv[2]
    bwt.writefile(fname,N)
    fc,lc,sa,digc,digv=build_FM(fname)
    encrypt_FM(fc,lc,sa,key,digc,digv,nonce)
    with open('key.pickle', 'wb') as handle:
      pickle.dump(key, handle, protocol=2)
    token(sys.argv[1],'key.pickle')
    return


if __name__=='__main__':
    main()
