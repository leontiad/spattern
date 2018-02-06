import random,string
from functools import total_ordering
from itertools import chain, islice
def rotations(t):
    ''' Return list of rotations of input string t '''
    tt = t * 2
    return [ tt[i:i+len(t)] for i in xrange(0, len(t)) ]

def bwm(t):
    return sorted(rotations(t))

def bwtViaBwm(t):
    ''' Given T, returns BWT(T) by way of the BWM '''
    return ''.join(map(lambda x: x[-1], bwm(t)))

def rankBwt(bw):
    ''' Given BWT string bw, return parallel list of B-ranks.  Also
        returns tots: map from character to # times it appears. '''
    tots = dict()
    ranks = []
    for c in bw:
        if c not in tots: tots[c] = 0
        ranks.append(tots[c])
        tots[c] += 1
    return ranks, tots
def firstCol(tots):
    ''' Return map from character to the range of rows prefixed by
        the character. '''
    first = {}
    totc = 0
    for c, count in sorted(tots.iteritems()):
        first[c] = (totc, totc + count)
        totc += count
    return first

def reverseBwt(bw):
    ''' Make T from BWT(T) '''
    ranks, tots = rankBwt(bw)
    first = firstCol(tots)
    rowi = 0 # start in first row
    t = '$' # start with rightmost character
    while bw[rowi] != '$':
        c = bw[rowi]
        t = c + t # prepend to answer
        # jump to row that starts with c of same rank
        rowi = first[c][0] + ranks[rowi]
    return t
def suffix_Array(A):

    L = sorted((a, i) for i, a in enumerate(A))
    n = len(A)
    count = 1
    while count < n:
        # Invariant: L is now a list of pairs such that L[i][1] is the
        # starting position in A of the i'th substring of length
        # 'count' in sorted order. (Where we imagine A to be extended
        # with dummy elements as necessary.)

        P = [0] * n
        for (r, i), (s, j) in zip(L, islice(L, 1, None)):
            P[j] = P[i] + (r != s)

        # Invariant: P[i] is now the position of A[i:i+count] in the
        # sorted list of unique substrings of A of length 'count'.

        L = sorted(chain((((P[i],  P[i+count]), i) for i in range(n - count)),
                         (((P[i], -1), i) for i in range(n - count, n))))
        count *= 2
    return [i for _, i in L]


def suffixArray(s):
    satups = sorted([(s[i:], i) for i in xrange(0, len(s))])
    #print (satups)
    return map(lambda x: x[1], satups)

def bwtViaSa(t,st,win):
    # Given T, returns BWT(T) by way of the suffix array
    bw = []
    fc = []
    sa=suffix_Array(t);
    #print sa
    cnt=1
    for si in sa:
        #if si == 0:
        #    bw.append('$')
        #else:
        bw.append(st[si-1:si-1+win])
        if cnt==1:
            fc.append(st[si-1:si+win])
        else:
            fc.append(st[si:si+win])
        cnt=cnt+1
    #fc=zip(fc,sa)
    #return
    #print 'bw='+str(bw)
    #print 'sa='+str(sa)
    #print 'fc='+str(fc)

    #return ''.join(bw),sa,fc # return string-ized version of list bw
    return bw,sa,fc # return string-ized version of list bw



def main():
    data=readfile('inp')
    b=bwtViaBwm(data)
    ranks,tots = rankBwt(b)
    '''print "Input stream = "+ data
    print "BWT = " + bwtViaSa(data)
    print '\n'.join(bwm(data))
    print ("Lc ranking:")
    print zip(b,ranks) 
    
    fc=[x[0] for x in bwm(data)]
    fc= ''.join(fc)
    print ("First column="+ fc)
    ranks,tots = rankBwt(fc)
    print("Fc ranking:")
    print zip(fc,ranks) 

    print reverseBwt(bwtViaSa(data))
'''


