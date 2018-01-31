from pyscipopt import Model
import random
import math
import filtersets
import fractions
from fractions import Fraction
import numpy as np
import cplex
import scipy.io
from copy import deepcopy
def allsets():
    allsets=[]
    for a in range(0,2):
        for b in range(0,2):
            for c in range(0,2):
                for d in range(0,2):
                    for e in range(0,2):
                        for f in range(0,2):
                            for g in range(0,2):
                                for h in range(0,2):
                                    for i in range(0,2):
                                        l=[a,b,c,d,e,f,g,h,i]
                                        allsets.insert(0,l)
    return allsets


def makeweightint(c):
    l=[x for x in allsets()]
    w = [round(x) for x in c]
    makeweight=[]
    for i in range(0,len(l)):
        print l[i]
        pos =  [i for i, e in enumerate(l[i]) if e != 0]
        neg=[]
        print pos
        print w
        print sum([w[x] for x in pos])
        for j in range(len(l[i])):
            if j not in pos:  
               neg.append(j)
        print neg
        print w
        print sum(w[x] for x in neg)
        makeweight.append(sum([w[x] for x in pos])-sum(w[x] for x in neg))
    return makeweight
def makeccoff(r):
    l=[x for x in allsets()]
    makecoeff=[0]*9
    for i in range(len(r)):
        if r[i]==1.0:
           for j in range(0,9):       
               if l[i][j]==1:
                  makecoeff[j]=makecoeff[j]+1
    return makecoeff

def makeccoffint(r):
    l=[x for x in allsets()]
    makecoeff=[0]*9
    for i in range(len(r)):
        if r[i]==1.0:
           for j in range(0,9):       
               if l[i][j]==1:
                  makecoeff[j]=makecoeff[j]+1
    return makecoeff


                 
def constraintsf(f):
    l=[x for x in allsets()]
    constraintsf=[]
    for i in range(len(f)):
        if f[i]!=0.0:
           
           for j in range(len(l)):
               if i!=j:
                 
                  k=l.index([max(l[i][0],l[j][0]), max(l[i][1],l[j][1]), max(l[i][2],l[j][2]), max(l[i][3],l[j][3]), max(l[i][4],l[j][4]), max(l[i][5],l[j][5]), max(l[i][6],l[j][6]), max(l[i][7],l[j][7]), max(l[i][8],l[j][8]), ])
                  if k!=j:
                    
                     constraintsf.append([j+1,k+1])
    return constraintsf

def constraints():
    l=[x for x in allsets()]
    constraints=[]
    for i in range(0,len(l)-1):
        for j in range(i+1, len(l)):
            k=l.index([max(l[i][0],l[j][0]), max(l[i][1],l[j][1]), max(l[i][2],l[j][2]), max(l[i][3],l[j][3]), max(l[i][4],l[j][4]), max(l[i][5],l[j][5]), max(l[i][6],l[j][6]), max(l[i][7],l[j][7]), max(l[i][8],l[j][8]),])
            if k != i:
               constraints.append([i+1,j+1,k+1])
    return constraints


def makenset(n):
    l=[x for x in allsets()]
    makenset=[]
    for elements in l:
        if sum(elements)==n:
           makenset.insert(0,elements)
    return makenset

def makenseti(n):
    l=[x for x in allsets()]
    makenseti=[]
    for elements in l:
        if sum(elements)==n:
           makenseti.insert(0,l.index(elements))
    return makenseti


def writingfunctionc(elist):
     f = open("writematrix", "w")
     for i in range(len(elist)+1):
         if i < len(elist):
            f.write(' \color{red}{%i} & ' %i)
         else:
            f.write(' \color{red}{%i} \\\ \n' %i)
     for j in range(len(elist[0])):
         for i in range(len(elist)+1):
             if i==0:
                d=j+1
                f.write('c_%d& ' %d)
             elif i < len(elist):
                k=i-1
                f.write(str(elist[k][j])+"& ")
             else:
                f.write(str(elist[k+1][j])+"\\\ \n")


def writingfunction(elist):
     ar=np.array(elist)
     ar=ar.T.tolist()
     num=[sum(ar[x]) for x in range(len(elist[0]))]
     f = open("writematrix", "w")
     for j in range(len(elist[0])):
         for i in range(len(elist)+1):
             if i==0:
                d=num[j]
                f.write(' \color{gray}{%d}& ' %d)
             elif i < len(elist):
                k=i-1
                f.write(str(elist[k][j])+"& ")
             else:
                f.write(str(elist[k+1][j])+"\\\ \n")


def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:      
        a, b = b, a % b
    return a

def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)

def lcmm(lst):
    """Return lcm of args."""   
    return reduce(lcm, lst)
def makeobj(c):
    l=[x for x in allsets()]
    cr = [Fraction(x).limit_denominator() for x in c]
    domw = [x.denominator for x in cr]
    multi = lcmm(domw)
    w = [2*multi*(x.numerator)/(x.denominator) for x in cr]
    makeweight=[]
    for i in range(0,len(l)):
        plusw=0
        for j in range(0,len(l[i])):
            if l[i][j]==1:
               plusw=plusw + w[j]
        makeweight.append(multi-plusw)
    return makeweight
def writefcfam(elist,one,a,b):
    f = open("fcfamilies", "a+")
    f.write(" \n")
    for i in range(len(elist)):
        if i >= 1:
           #print i
           counter = 0 
           for j in range(len(elist[i])):
               #print j
               d = j +1
               m = sum(elist[i])
               if j == 0 and i == 1:
                  f.write('\pbox{20cm}{[')
               if elist[i][j] ==1:
                 
                  f.write('%d' %d)
               if a != 0 and b == 0:
                  if j == len(elist[i])-1 and i != (len(elist)-1) and i !=a:
                     f.write(', ')
                  if j == len(elist[i])-1 and i != (len(elist)-1) and i == a :
                     f.write(', \\\\ ')
               if a != 0 and b != 0:
                  if j == len(elist[i])-1 and i != (len(elist)-1) and i !=a and i != b:
                     f.write(', ')
                  if j == len(elist[i])-1 and i != (len(elist)-1) and (i == a or i == b):
                     f.write(', \\\\ ')
               if j == len(elist[i])-1 and i != (len(elist)-1):
                     f.write(', ')
               if i == (len(elist)-1) and j == (len(elist[i])-1) and one ==0:
                 # print 'last one please'
                  f.write(']*} & ')
               if i == (len(elist)-1) and j == (len(elist[i])-1) and one ==1:
                 # print 'last one please'
                  f.write(']*} & \scriptsize{ ')
    for i in range(len(elist[0])):
         #d = elist[0][i]
         n=i+1
         if i != len(elist[0]) -1:
            f.write('$ ' )
            f.write('%i ' %(i+1))
            f.write(' \mapsto ')
            f.write('%i' %elist[0][i])
            f.write('$, ')
         elif one == 0:
            f.write('$ ' )
            f.write('%i ' %(i+1))
            f.write(' \mapsto ')
            f.write('%i' %elist[0][i])
            f.write('$ \\\\\hline')
         else:
            f.write('$ ' )
            f.write('%i ' %(i+1))
            f.write(' \mapsto ')
            f.write('%i' %elist[0][i])
            f.write('$} \\\\\hline')
    f.close()

def allsetsmall(n):
    one=[]
   
    for i in range(n):
        biggie = filtersets.powerset(n)
        for j in range(len(biggie)):
            biggie[j].insert(i,0)
        one.insert(0,biggie)
    return one
def makesab(elist,n):
    fin = []
    p = [x for x in allsets()]
    small = allsetsmall(n)
    for i in range(len(small)):
        one = []
        for j in range(len(small[i])):
             for k in range(len(elist)):
                 one.insert(0,filtersets.makeUnion(small[i][j],elist[k]))
        keep = list(map(list, set(map(lambda i: tuple(i),one))))
        if filtersets.checkUnionClosed(keep) == 0:
           return 'fucked up'
        keep = [p.index(x) for x in keep]
        fina = [0]*len(p)
        for i in range(len(keep)):
             fina[keep[i]]=1
        fin.insert(0,fina)
   
       
         
    return fin
        
def scipfamily9generalconj(ll,fixer):
    biggig =[]
    for g in range(len(ll)):
        l = [x for x in constraints()]
        p = [x for x in allsets()]
        weight=[1.0,1.0,-1.0]
        oweight=[1.0,-1.0]
        for i in range(len(l)):
            new=l[i] + weight
        c = [6,6,6,6,6,5,6,7,8]  
        cone = [0,100,41,39,40,27,89,91,111]  
        if fixer == 1:
           two = filtersets.zerone(ll[g])
        else:  
           two = ll[g]
        sets=two
        indexkeeps = filtersets.powerset(9)
        allones=[1.0]*len(p)
        flag=1
        count=0
        index=[]
        fixf = Model()
        fixf.hideOutput()
        fixf.setMinimize()
   
        FranklVarsf = []
        FvarNamesf = []
        FvarBaseNamef = "Setfix"
        # add frankl variables
        for i in range(len(p)):
            FvarNamesf.append(FvarBaseNamef + "_" + str(i))
            FranklVarsf.append(fixf.addVar(FvarNamesf[i], vtype='B', obj=1.0, ub=1.0))
        # add union-closed constraints
        for i in range(len(l)):
            new=l[i] + weight
            coeffs = {FranklVarsf[l[i][j]-1]: new[j+3] for j in range(0,len(weight))}
            fixf.addCons(coeffs, lhs=None, rhs=1.0, name ="uc(%s)" %i)
        # add fixed family
        for i in range(len(sets)):
            coeffs = {FranklVarsf[p.index(sets[i])]: 1.0}
            fixf.addCons(coeffs, lhs = 1.0, rhs = 1.0)
        
        fixf.optimize()
        fixedfam=[0.0]*len(p)
        if fixf.getStatus()=="optimal":
           for j in range(len(p)):
               fixedfam[j]=round(fixf.getVal(FranklVarsf[j]))
                  
        else:
           print 'We have a bug in the generation of the fixed family'  
        lf = [x for x in constraintsf(fixedfam)]
        onemore = []
        myfam = []
        for i in range(len(fixedfam)):
            if fixedfam[i] > 0.5:
               onemore.insert(0,indexkeeps.index(p[i]))
               myfam.insert(0,p[i])
       
        print onemore
        #myfam = [p[x] for x in onemore]
        print myfam
        index = makesab(myfam,9)
        print 'my index of thingsss'
        print index
        fixf.free()  
        while flag==1:
          # continous model for c_is
          slin = Model()
          slin.hideOutput()
          # binary model for fixed c_i
          sbin = Model()
          sbin.setMinimize()
          #sbin.setIntParam("limits/solutions", 1)
          sbin.hideOutput()
          #sbin.setMaximize()
          # continous variables c_is
          WeightVars = []
          WvarNames = []
          WvarBaseName = "Weight"
          # binary variables for sets in frankl family
          FranklVars = []
          FvarNames = []
          FvarBaseName = "x"
   
          # add c_i variables
          for i in range(len(c)):
              if i <=7:
                 WvarNames.append(WvarBaseName + "_"+ str(i))
                 WeightVars.append(slin.addVar(WvarNames[i], vtype='I', obj=1.0, lb=0.0))
              else:
                 WvarNames.append(WvarBaseName + "_" + str(i))
                 WeightVars.append(slin.addVar(WvarNames[i], vtype='I', obj=1.0, lb=0.0))
          # add constraints sum equals one
          coeffs = [1]*len(c)
          #coeffs1 = [1]
          objec = {WeightVars[i]: coeffs[i] for i in range(len(c))}
          slin.setObjective(objec,"minimize")
          coeffss = {WeightVars[i]: 1.0 for i in range(len(c))}
          #coeffss1 = {WeightVars[i]: 1.0 for i in range(5,6)}
          slin.addCons(coeffss, lhs=1.0, rhs=None,name= 'sum_one')
          #slin.addCons(coeffss1,lhs=0.0, rhs=0.0,name= 'fix_one')
          if count == 0:
             for i in range(len(index)):
                 size=sum(index[i])
                 print size
                 print 'hereererere'
                 keeperset=[]
                 for j in range(len(index[i])):
                     if index[i][j] >= 0.5:
                        keeperset.insert(0,j)
                 print count 
                 print [indexkeeps.index(p[x]) for x in keeperset]
                 cr=[x for x in makeccoff(index[i])]
                 coeffs = {WeightVars[j]: (2*cr[j]-size) for j in range(len(cr))}
                 slin.addCons(coeffs, lhs=0.0, rhs=None,name= 'nogoodcut')

          if count >= 1:
             print count
            # print 'this is it!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1'
             #print makeccoff(index[0])
            # print index[0]
             # print 'this is it!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1'
            # print index
             for i in range(len(index)):
                 size=sum(index[i])
                 print size
                 print 'hereererere'
                 keeperset=[]
                 for j in range(len(index[i])):
                     if index[i][j] >= 0.5:
                        keeperset.insert(0,j)
                 print count 
                 print [indexkeeps.index(p[x]) for x in keeperset]
                 cr=[x for x in makeccoff(index[i])]
                 coeffs = {WeightVars[j]: (2*cr[j]-size) for j in range(len(cr))}
                 slin.addCons(coeffs, lhs=0.0, rhs=None,name= 'nogoodcut')

          
          # optimize linear program with c_is
          # slin.hideOutput()
          slin.optimize()
         
          # get best solution
          # csol=slin.getBestSol 
          
          if slin.getStatus()=="optimal":  # if we find optimal print c
             for i in range(len(c)):
                 c[i]=slin.getVal(WeightVars[i])
             #print c
          else:
              flag=0                       # otherwise we found a proof!
              print 'Found Infeasibility'
              slin.writeProblem('check.lp')
              
              for i in range(len(c)):
                  c[i]=slin.getVal(WeightVars[i])
              print c
              break
              #return 0
              
          slin.free()
          # add frankl variables
          for i in range(len(p)):
              FvarNames.append(FvarBaseName + "_" + str(i))
              FranklVars.append(sbin.addVar(FvarNames[i], vtype='B', obj=1.0, ub=1.0))
  
          # add union-closed constraints
          for i in range(len(l)):
              new=l[i] + weight
              coeffs = {FranklVars[l[i][j]-1]: new[j+3] for j in range(0,len(weight))}
              sbin.addCons(coeffs, lhs=None, rhs=1.0, name ="uc(%s)" %i)
          coeffs = {FranklVars[i]: allones[i] for i in range(len(p))}
          #sbin.addCons(coeffs, lhs=1, rhs=None, name= 'mini')
          # add fixed family constraints
         
          for i in range(len(lf)):
              new=lf[i] + oweight
              coeffs = {FranklVars[lf[i][j]-1]: new[j+2] for j in range(0,len(oweight))}
              sbin.addCons(coeffs, lhs=None, rhs=0.0, name= "fs(%s)" %i)
         
          #weits=makeweightint(c)
          #num=weits[0]
          
         
          num=[x for x in makeweightint(c)]
          obj=[x for x in makeobj(c)]
          # print num
          # add feasibility constraint
          coeffs = {FranklVars[i]: num[i] for i in range(len(p))}
          obj = {FranklVars[i]: obj[i] for i in range(len(p))}
          sbin.setObjective(obj,"maximize")
          sbin.addCons(coeffs, lhs = None, rhs = -1)
          sbin.setMaximize()
          sbin.writeProblem('checkIP.lp')
          spx = cplex.Cplex()
          spx.read('checkIP.lp')
          #spx.parameters.mip.limits.solutions.set(1)
          spx.set_log_stream(None)
          spx.set_error_stream(None)
          spx.set_warning_stream(None)
          spx.set_results_stream(None)
          spx.solve()
          
         
          # optimize binary program
          # sbin.setMaximize()
          
          # sbin.optimize()
          row=[None]*len(p)
          rwo=[]
          rwo1=[]
         
          if spx.solution.get_status() == 101 or spx.solution.get_status()==102:
             allguys = filtersets.powerset(9)
             Aguy = [allguys[x] for x in onemore]
             Aguy.reverse()
             #print onemore
           
             for j in range(len(p)):
                 row[j]=round(spx.solution.get_values(j))
             #print row
             for j in range(len(p)):
                 if round(spx.solution.get_values(j))>= 0.5:
                    rwo1.insert(0,indexkeeps.index(p[j]))
                    rwo.insert(0,j)
             rwo
             #print rwo
             Bguy = [allguys[x] for x in rwo1] 
             Bguy
             print onemore
             print rwo
             totsum = sum([num[x] for x in rwo])
             A = filtersets.checkUnionClosed(Bguy)  
             B = filtersets.checkABunionClosed(Aguy,Bguy) 
             if A==1 and B==1 and totsum <= -1:
                #print row
                index.insert(0,row)
             else:
                print A
                print B
                print totsum
                return 'fucked up solution'
          else:
             print 'We found the suckers!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'  # we found a proof!
             print c
             print [Fraction(x).limit_denominator() for x in c]
             sbin.writeProblem('checkIP.lp')
             kepme= [Fraction(x).limit_denominator().numerator for x in c]
             setsc = deepcopy(two)
             setsc.insert(0,kepme)
             print kepme
             #print 'werrrerrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
             #return setsc
             flag = 0
             biggig.insert(0,kepme)
             biggig.insert(0,g)
            
          count=count+1
          sbin.free()
    return biggig                 

    
    
def scipfamily9general(ll,fixer):
    biggig =[]
    for g in range(len(ll)):
        l = [x for x in constraints()]
        p = [x for x in allsets()]
        weight=[1.0,1.0,-1.0]
        oweight=[1.0,-1.0]
        for i in range(len(l)):
            new=l[i] + weight
        c = [6,6,6,6,6,5,6,7,8]  
        cone = [0,100,41,39,40,27,89,91,111]  
        if fixer == 1:
           two = filtersets.zerone(ll[g])
        else:  
           two = ll[g]
        sets=two
        indexkeeps = filtersets.powerset(9)
        allones=[1.0]*len(p)
        flag=1
        count=0
        index=[]
        fixf = Model()
        fixf.hideOutput()
        fixf.setMinimize()
   
        FranklVarsf = []
        FvarNamesf = []
        FvarBaseNamef = "Setfix"
        # add frankl variables
        for i in range(len(p)):
            FvarNamesf.append(FvarBaseNamef + "_" + str(i))
            FranklVarsf.append(fixf.addVar(FvarNamesf[i], vtype='B', obj=1.0, ub=1.0))
        # add union-closed constraints
        for i in range(len(l)):
            new=l[i] + weight
            coeffs = {FranklVarsf[l[i][j]-1]: new[j+3] for j in range(0,len(weight))}
            fixf.addCons(coeffs, lhs=None, rhs=1.0, name ="uc(%s)" %i)
        # add fixed family
        for i in range(len(sets)):
            coeffs = {FranklVarsf[p.index(sets[i])]: 1.0}
            fixf.addCons(coeffs, lhs = 1.0, rhs = 1.0)
        
        fixf.optimize()
        fixedfam=[0.0]*len(p)
        if fixf.getStatus()=="optimal":
           for j in range(len(p)):
               fixedfam[j]=round(fixf.getVal(FranklVarsf[j]))
                  
        else:
           print 'We have a bug in the generation of the fixed family'  
        lf = [x for x in constraintsf(fixedfam)]
        onemore = []
        for i in range(len(fixedfam)):
            if fixedfam[i] > 0.5:
               onemore.insert(0,indexkeeps.index(p[i]))
        print onemore
        fixf.free()  
        while flag==1:
          # continous model for c_is
          slin = Model()
          slin.hideOutput()
          # binary model for fixed c_i
          sbin = Model()
          sbin.setMinimize()
          #sbin.setIntParam("limits/solutions", 1)
          sbin.hideOutput()
          #sbin.setMaximize()
          # continous variables c_is
          WeightVars = []
          WvarNames = []
          WvarBaseName = "Weight"
          # binary variables for sets in frankl family
          FranklVars = []
          FvarNames = []
          FvarBaseName = "x"
   
          # add c_i variables
          for i in range(len(c)):
              if i <=7:
                 WvarNames.append(WvarBaseName + "_"+ str(i))
                 WeightVars.append(slin.addVar(WvarNames[i], vtype='I', obj=1.0, lb=0.0))
              else:
                 WvarNames.append(WvarBaseName + "_" + str(i))
                 WeightVars.append(slin.addVar(WvarNames[i], vtype='I', obj=1.0, lb=0.0))
          # add constraints sum equals one
          coeffs = [1]*len(c)
          #coeffs1 = [1]
          objec = {WeightVars[i]: coeffs[i] for i in range(len(c))}
          slin.setObjective(objec,"minimize")
          coeffss = {WeightVars[i]: 1.0 for i in range(len(c))}
          #coeffss1 = {WeightVars[i]: 1.0 for i in range(5,6)}
          slin.addCons(coeffss, lhs=1.0, rhs=None,name= 'sum_one')
          #slin.addCons(coeffss1,lhs=0.0, rhs=0.0,name= 'fix_one')
          
          if count >= 1:
             print count
            # print 'this is it!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1'
             #print makeccoff(index[0])
            # print index[0]
             # print 'this is it!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1'
            # print index
             for i in range(len(index)):
                 size=sum(index[i])
                 print size
                 print 'hereererere'
                 keeperset=[]
                 for j in range(len(index[i])):
                     if index[i][j] >= 0.5:
                        keeperset.insert(0,j)
                 print count 
                 print [indexkeeps.index(p[x]) for x in keeperset]
                 cr=[x for x in makeccoff(index[i])]
                 coeffs = {WeightVars[j]: (2*cr[j]-size) for j in range(len(cr))}
                 slin.addCons(coeffs, lhs=0.0, rhs=None,name= 'nogoodcut')

          
          # optimize linear program with c_is
          # slin.hideOutput()
          slin.optimize()
         
          # get best solution
          # csol=slin.getBestSol 
          
          if slin.getStatus()=="optimal":  # if we find optimal print c
             for i in range(len(c)):
                 c[i]=slin.getVal(WeightVars[i])
             #print c
          else:
              flag=0                       # otherwise we found a proof!
              print 'Found Infeasibility'
              slin.writeProblem('check.lp')
              
              for i in range(len(c)):
                  c[i]=slin.getVal(WeightVars[i])
              print c
              break
              #return 0
              
          slin.free()
          # add frankl variables
          for i in range(len(p)):
              FvarNames.append(FvarBaseName + "_" + str(i))
              FranklVars.append(sbin.addVar(FvarNames[i], vtype='B', obj=1.0, ub=1.0))
  
          # add union-closed constraints
          for i in range(len(l)):
              new=l[i] + weight
              coeffs = {FranklVars[l[i][j]-1]: new[j+3] for j in range(0,len(weight))}
              sbin.addCons(coeffs, lhs=None, rhs=1.0, name ="uc(%s)" %i)
          coeffs = {FranklVars[i]: allones[i] for i in range(len(p))}
          #sbin.addCons(coeffs, lhs=1, rhs=None, name= 'mini')
          # add fixed family constraints
         
          for i in range(len(lf)):
              new=lf[i] + oweight
              coeffs = {FranklVars[lf[i][j]-1]: new[j+2] for j in range(0,len(oweight))}
              sbin.addCons(coeffs, lhs=None, rhs=0.0, name= "fs(%s)" %i)
         
          #weits=makeweightint(c)
          #num=weits[0]
          
         
          num=[x for x in makeweightint(c)]
          obj=[x for x in makeobj(c)]
          # print num
          # add feasibility constraint
          coeffs = {FranklVars[i]: num[i] for i in range(len(p))}
          obj = {FranklVars[i]: obj[i] for i in range(len(p))}
          sbin.setObjective(obj,"maximize")
          sbin.addCons(coeffs, lhs = None, rhs = -1)
          sbin.setMaximize()
          sbin.writeProblem('checkIP.lp')
          spx = cplex.Cplex()
          spx.read('checkIP.lp')
          #spx.parameters.mip.limits.solutions.set(1)
          spx.set_log_stream(None)
          spx.set_error_stream(None)
          spx.set_warning_stream(None)
          spx.set_results_stream(None)
          spx.solve()
          
         
          # optimize binary program
          # sbin.setMaximize()
          
          # sbin.optimize()
          row=[None]*len(p)
          rwo=[]
          rwo1=[]
         
          if spx.solution.get_status() == 101 or spx.solution.get_status()==102:
             allguys = filtersets.powerset(9)
             Aguy = [allguys[x] for x in onemore]
             Aguy.reverse()
             #print onemore
           
             for j in range(len(p)):
                 row[j]=round(spx.solution.get_values(j))
             #print row
             for j in range(len(p)):
                 if round(spx.solution.get_values(j))>= 0.5:
                    rwo1.insert(0,indexkeeps.index(p[j]))
                    rwo.insert(0,j)
             rwo
             #print rwo
             Bguy = [allguys[x] for x in rwo1] 
             Bguy
             print onemore
             print rwo
             totsum = sum([num[x] for x in rwo])
             A = filtersets.checkUnionClosed(Bguy)  
             B = filtersets.checkABunionClosed(Aguy,Bguy) 
             if A==1 and B==1 and totsum <= -1:
                #print row
                index.insert(0,row)
             else:
                print A
                print B
                print totsum
                return 'fucked up solution'
          else:
             print 'We found the suckers!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'  # we found a proof!
             print c
             print [Fraction(x).limit_denominator() for x in c]
             sbin.writeProblem('checkIP.lp')
             kepme= [Fraction(x).limit_denominator().numerator for x in c]
             setsc = deepcopy(two)
             setsc.insert(0,kepme)
             print kepme
             #print 'werrrerrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
             #return setsc
             flag = 0
             biggig.insert(0,kepme)
             biggig.insert(0,g)
            
          count=count+1
          sbin.free()
    return biggig
       
def scipfamily9generalmini(ll,fixer,one):
    biggig=[]
    l = [x for x in constraints()]
    p = [x for x in allsets()]
    weight=[1.0,1.0,-1.0]
    oweight=[1.0,-1.0]
    for i in range(len(l)):
        new=l[i] + weight
    c = [6,6,6,6,6,5,6,7,9]  
    cone = [0,100,41,39,40,27,89,91,111]  
    if fixer == 1:
        two1 = filtersets.zerone(ll)
    else:  
        two1 = ll
    two = []
    for i in range(len(two1)):
        if i != one:
           two.insert(0,two1[i])
    sets=two
    indexkeeps = filtersets.powerset(9)
    allones=[1.0]*len(p)
    flag=1
    count=0
    index=[]
    fixf = Model()
    fixf.hideOutput()
    fixf.setMinimize()
   
    FranklVarsf = []
    FvarNamesf = []
    FvarBaseNamef = "Setfix"
    # add frankl variables
    for i in range(len(p)):
        FvarNamesf.append(FvarBaseNamef + "_" + str(i))
        FranklVarsf.append(fixf.addVar(FvarNamesf[i], vtype='B', obj=1.0, ub=1.0))
    # add union-closed constraints
    for i in range(len(l)):
        new=l[i] + weight
        coeffs = {FranklVarsf[l[i][j]-1]: new[j+3] for j in range(0,len(weight))}
        fixf.addCons(coeffs, lhs=None, rhs=1.0, name ="uc(%s)" %i)
    # add fixed family
    for i in range(len(sets)):
          coeffs = {FranklVarsf[p.index(sets[i])]: 1.0}
          fixf.addCons(coeffs, lhs = 1.0, rhs = 1.0)
             # if i >=6 and i <=7:
               #  coeffs = {FranklVars[p.index(sets[i])]: 1.0}
                # sbin.addCons(coeffs, lhs = 1.0, rhs = 1.0)

      # add the empty set
   
    #fixf.writeProblem('original.lp')
    fixf.optimize()
    fixedfam=[0.0]*len(p)
    if fixf.getStatus()=="optimal":
             for j in range(len(p)):
                 fixedfam[j]=round(fixf.getVal(FranklVarsf[j]))
                  
            

    else:
        print 'We have a bug in the generation of the fixed family'  
    lf = [x for x in constraintsf(fixedfam)]
   
    onemore = []
    for i in range(len(fixedfam)):
        if fixedfam[i] > 0.5:
           onemore.insert(0,indexkeeps.index(p[i]))
    print onemore
    #print [x for x in p if fixedfam[p.index(x)] > 0.0]
    #return 0
    fixf.free()  
    while flag==1:
          # continous model for c_is
          slin = Model()
          slin.hideOutput()
          # binary model for fixed c_i
          sbin = Model()
          sbin.setMinimize()
          #sbin.setIntParam("limits/solutions", 1)
          sbin.hideOutput()
          #sbin.setMaximize()
          # continous variables c_is
          WeightVars = []
          WvarNames = []
          WvarBaseName = "Weight"
          # binary variables for sets in frankl family
          FranklVars = []
          FvarNames = []
          FvarBaseName = "x"
   
          # add c_i variables
          for i in range(len(c)):
              if i <=7:
                 WvarNames.append(WvarBaseName + "_"+ str(i))
                 WeightVars.append(slin.addVar(WvarNames[i], vtype='I', obj=1.0, lb=0.0))
              else:
                 WvarNames.append(WvarBaseName + "_" + str(i))
                 WeightVars.append(slin.addVar(WvarNames[i], vtype='I', obj=1.0, lb=0.0))
          # add constraints sum equals one
          coeffs = [1]*len(c)
          #coeffs1 = [1]
          objec = {WeightVars[i]: coeffs[i] for i in range(len(c))}
          slin.setObjective(objec,"minimize")
          coeffss = {WeightVars[i]: 1.0 for i in range(len(c))}
          #coeffss1 = {WeightVars[i]: 1.0 for i in range(5,6)}
          slin.addCons(coeffss, lhs=1.0, rhs=None,name= 'sum_one')
          #slin.addCons(coeffss1,lhs=0.0, rhs=0.0,name= 'fix_one')
          
          if count >= 1:
             print count
            # print 'this is it!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1'
             #print makeccoff(index[0])
            # print index[0]
             # print 'this is it!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1'
            # print index
             for i in range(len(index)):
                 size=sum(index[i])
                 print size
                 print 'hereererere'
                 keeperset=[]
                 for j in range(len(index[i])):
                     if index[i][j] >= 0.5:
                        keeperset.insert(0,j)
                 print count 
                 print [indexkeeps.index(p[x]) for x in keeperset]
                 cr=[x for x in makeccoff(index[i])]
                 coeffs = {WeightVars[j]: (2*cr[j]-size) for j in range(len(cr))}
                 slin.addCons(coeffs, lhs=0.0, rhs=None,name= 'nogoodcut')

          
          # optimize linear program with c_is
          # slin.hideOutput()
          slin.optimize()
         
          # get best solution
          # csol=slin.getBestSol 
          
          if slin.getStatus()=="optimal":  # if we find optimal print c
             for i in range(len(c)):
                 c[i]=slin.getVal(WeightVars[i])
             #print c
          else:
              flag=0                       # otherwise we found a proof!
              print 'Found Infeasibility'
              slin.writeProblem('check.lp')
              
              for i in range(len(c)):
                  c[i]=slin.getVal(WeightVars[i])
              print c
              return 0
              
          slin.free()
          # add frankl variables
          for i in range(len(p)):
              FvarNames.append(FvarBaseName + "_" + str(i))
              FranklVars.append(sbin.addVar(FvarNames[i], vtype='B', obj=1.0, ub=1.0))
  
          # add union-closed constraints
          for i in range(len(l)):
              new=l[i] + weight
              coeffs = {FranklVars[l[i][j]-1]: new[j+3] for j in range(0,len(weight))}
              sbin.addCons(coeffs, lhs=None, rhs=1.0, name ="uc(%s)" %i)
          coeffs = {FranklVars[i]: allones[i] for i in range(len(p))}
          #sbin.addCons(coeffs, lhs=1, rhs=None, name= 'mini')
          # add fixed family constraints
         
          for i in range(len(lf)):
              new=lf[i] + oweight
              coeffs = {FranklVars[lf[i][j]-1]: new[j+2] for j in range(0,len(oweight))}
              sbin.addCons(coeffs, lhs=None, rhs=0.0, name= "fs(%s)" %i)
         
          #weits=makeweightint(c)
          #num=weits[0]
          
         
          num=[x for x in makeweightint(c)]
          obj=[x for x in makeobj(c)]
          # print num
          # add feasibility constraint
          coeffs = {FranklVars[i]: num[i] for i in range(len(p))}
          obj = {FranklVars[i]: obj[i] for i in range(len(p))}
          sbin.setObjective(obj,"maximize")
          sbin.addCons(coeffs, lhs = None, rhs = -1)
          sbin.setMaximize()
          sbin.writeProblem('checkIP.lp')
          spx = cplex.Cplex()
          spx.read('checkIP.lp')
          #spx.parameters.mip.limits.solutions.set(1)
          spx.set_log_stream(None)
          spx.set_error_stream(None)
          spx.set_warning_stream(None)
          spx.set_results_stream(None)
          spx.solve()
          
         
          # optimize binary program
          # sbin.setMaximize()
          
          # sbin.optimize()
          row=[None]*len(p)
          
         
          if spx.solution.get_status() == 101 or spx.solution.get_status() == 102:
             for j in range(len(p)):
                 row[j]=round(spx.solution.get_values(j))
                 

             index.insert(0,row)
          else:
             print 'We found the suckers!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'  # we found a proof!
             print c
             print [Fraction(x).limit_denominator() for x in c]
             sbin.writeProblem('checkIP.lp')
             kepme= [Fraction(x).limit_denominator().numerator for x in c]
             print kepme
             print 'werrrerrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
             biggig.insert(0,one)
             flag = 0
          count=count+1
          sbin.free()
    print biggig             
              
             









