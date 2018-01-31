import math
import itertools
import igraph
import numpy as np
import cairo
from copy import deepcopy

def makeMNsets(N,M):
    sets = [x for x in map(list, itertools.product([0, 1], repeat=N)) if sum(x) == M]
    return sets

def powerset(n):
    powerset = [x for x in map(list, itertools.product([0, 1], repeat = n))]
    return powerset
#################################################################################################################################
# given the set pset represented as a list, generate all k subsets of pset
def makeKsets(pset,k):
    sets = map(list, itertools.combinations(pset,k))
    return sets

# given sets fist and second represented as lists with 0/1 entries generate their union
def makeUnion(first,second):
    # add first and second element wise and divide by 2 if sum of elements is 2
    union = [element/2 if element == 2 else element for element in [sum(x) for x in zip(first,second)]]
    return union
def zerone(lists):
    oneguy = []
    for i in range(len(lists)):
        one = []
        for j in range(len(lists[i])):
              if lists[i][j] == 0:
                 one.insert(0,1)
              if lists[i][j] == 1:
                 one.insert(0,0)
        oneguy.insert(0,one)
    return oneguy
def makeprime(ls):
    weight = 1
    primes = [2,3,4,5,7,11,13,17,19]
    if sum(ls)==0:
       weight = weight*0;
    else:
       for i in range(len(ls)):
             if ls[i]==1:
                weight=weight*primes[i]
    return weight
def partition(number):
    answer = set()
    answer.add((number, ))
    for x in range(1, number):
         for y in partition(number - x):
            answer.add(tuple(sorted((x, ) + y)))
    return list(answer)
def checkUnionClosed(ll):
    keepprime = [makeprime(x) for x in ll]
    for i in range(len(ll)-1):
        for j in range(i+1,len(ll)):
            if makeprime(makeUnion(ll[i],ll[j])) not in keepprime:
               print i
               print j
               print 'we are here'
               return 0
    return 1

def revnlis(elist,n):
    bigs=[]
    for i in range(len(elist)):
         zero = [0]*n
         one=list(map(int,str(elist[i])))
         for j in range(len(one)):
             zero[one[j]-1]=1
         bigs.insert(0,zero)
    return bigs

def checkABunionClosed(l1,l2):
    checkUnionClosed(l1)
    checkUnionClosed(l2)
    keepprime = [makeprime(x) for x in l2]
    for i in range(len(l1)):
        for j in range(len(l2)):
            if makeprime(makeUnion(l1[i],l2[j])) not in keepprime:
               print i
               print j
               print 'second one'
               return 0
    return 1
    
             
def getKoutMNsets(N,M,K):
    sets = map(list, itertools.combinations(makeMNsets(N,M),K))
    sets = filter(is_zero,sets)
    return sets

def getKoutMNsetsx(N,M,K):
    sets = map(list, itertools.combinations(makeMNsets(N,M),K))
    return sets

def zero(x):
    if 0 not in x:
       return 1
    return 0
       
def is_zero(x):
    x = [x]
    y = mergesets(x)
    y = y[0]
    return zero(y)

def mergeKoutMNsets(N,M,K):
    KoutMNsets = getKoutMNsets(N,M,K)
    sets = []
    for i in range(len(KoutMNsets)):

           sets.append([sum(x) for x in zip(*KoutMNsets[i])])
           
    return sets

def mergesets(sets):
    msets=[]
    for i in range(len(sets)):
          msets.append([sum(x) for x in zip(*sets[i])])
           
    return msets


def makegraph(sets,N,K):
    zerosone = np.zeros((K,K),dtype=np.int)
    zerostwo = np.zeros((N,N),dtype=np.int)
    a = np.array(sets)
    atrans = a.T
    lowerhalfone=np.concatenate((a,zerosone),axis=1)
    upperhalfone=np.concatenate((zerostwo,atrans),axis=1)
    finalone=np.concatenate((upperhalfone,lowerhalfone),axis=0)
    g = igraph.Graph.Adjacency(finalone.tolist()) 
    return g     

def checkiso(sets,N,K):
    index=[-1]*len(sets)
    bigkeeper = []
    zerosone = np.zeros((K,K),dtype=np.int)
    zerostwo = np.zeros((N,N),dtype=np.int)
    for i in range(len(sets)):
        #print 'We are at sets %i' %i
        if index[i]==-1:
           index[i]=i
           keeper = []
           a = np.array(sets[i])
           atrans = a.T
           lowerhalfone=np.concatenate((a,zerosone),axis=1)
           upperhalfone=np.concatenate((zerostwo,atrans),axis=1)
           finalone=np.concatenate((upperhalfone,lowerhalfone),axis=0)
           g = igraph.Graph.Adjacency(finalone.tolist())
           for j in range(i+1,len(sets)):
               d=j
              # print 'checking %d' %d
               if index[j] == -1:
                  b = np.array(sets[j])
                  btrans = b.T
                  lowerhalftwo=np.concatenate((b,zerosone),axis=1)
                  upperhalftwo=np.concatenate((zerostwo,btrans),axis=1)
                  finaltwo=np.concatenate((upperhalftwo,lowerhalftwo),axis=0)  
                  gb = igraph.Graph.Adjacency(finaltwo.tolist())
                  if g.isomorphic(gb):
                    # print 'found one %d' %d
                     keeper.append(j)
                     index[j]=i
           #print keeper
           bigkeeper.insert(0,keeper)
           myguy = np.unique(index)
    return myguy.tolist(),bigkeeper
        
def checkisoadd(sets,addsets,N,M,K):
    keepsets=[]
    bigcopy=[]
    for i in range(len(addsets)):
        bigcopy.insert(0,deepcopy(sets))

    for j in range(len(sets)):
        for i in range(len(addsets)):
            for l in range(len(addsets[i])):
                counter=0  
                if addsets[i][l] in sets[j]:
                   counter=counter+1
            if counter == 0:
               for k in range(len(addsets[i])):
                   bigcopy[i][j].insert(0,addsets[i][k])
    keepsets=[bigcopy[i][j] for i in range(len(addsets)) for j in range(len(sets)) if len(bigcopy[i][j])==K]
        
    index=[-1]*len(keepsets)
    bigkeeper = []
    zerosone = np.zeros((K,K),dtype=np.int)
    zerostwo = np.zeros((N,N),dtype=np.int)
    for i in range(len(keepsets)):
        #print 'We are at sets %i' %i
        if index[i]==-1:
           index[i]=i
           keeper = []
           a = np.array(keepsets[i])
           #print a
           atrans = a.T
           lowerhalfone=np.concatenate((a,zerosone),axis=1)
           upperhalfone=np.concatenate((zerostwo,atrans),axis=1)
           finalone=np.concatenate((upperhalfone,lowerhalfone),axis=0)
           g = igraph.Graph.Adjacency(finalone.tolist())
           for j in range(i+1,len(keepsets)):
               d=j
               #print 'checking %d' %d
               if index[j] == -1:
                  b = np.array(keepsets[j])
                  btrans = b.T
                  lowerhalftwo=np.concatenate((b,zerosone),axis=1)
                  upperhalftwo=np.concatenate((zerostwo,btrans),axis=1)
                  finaltwo=np.concatenate((upperhalftwo,lowerhalftwo),axis=0)  
                  gb = igraph.Graph.Adjacency(finaltwo.tolist())
                  if g.isomorphic(gb):
                    # print 'found one %d' %d
                     keeper.append(j)
                     index[j]=i
          # print keeper
           bigkeeper.insert(0,keeper)
           myguy = np.unique(index)
    final=getKoutMNsets(N,M,K)
    intermediate = [keepsets[x] for x in myguy.tolist()]
    return intermediate, bigkeeper

             
