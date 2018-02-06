import pickle,sys,utils

def search(encfm,tok):
    efm,llset=utils.loadIndex(encfm)
   # tok=utils.loadSinglePickle(token)

    #take all the lc from fc
    fset=[]
    if tok[-1] in llset:
        fset=llset[tok[-1]]
    if not fset:
        print("Token not found and stopped at first iteration")
        return
    
    #get correctness for second element from last column 
    for en,tt in enumerate(reversed(tok[:-1])):
        for idx,x in enumerate(fset):
            if efm[x][0]!=tt:
                del fset[idx]
        if en==len(tok)-2:#token found
            return [efm[y][2] for y in fset]
        else:
            keys=[utils.xor_strings(efm[k][0],efm[k][1]) for k in fset]
            del fset[:]
            fset=keys


'''Usage python cloud.py encefm.pickle token.pickle key.pickle'''
if __name__=='__main__':
    key=utils.loadSinglePickle("key.pickle")
    res=search(sys.argv[1],sys.argv[2])
    print([utils.decryptbox(x,key) for x in res])
