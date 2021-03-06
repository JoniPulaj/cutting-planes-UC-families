from pyscipopt import Model
import random
import math
import filtersets
import fractions
from fractions import Fraction
import numpy as np
import cplex
import scipy.io
import re
from copy import deepcopy

# generate power set
def allsets():
    allsets=[]
    for a in range(0,2):
        for b in range(0,2):
            for c in range(0,2):
                for d in range(0,2):
                    for e in range(0,2):
                        for f in range(0,2):
                            l=[a,b,c,d,e,f]
                            allsets.insert(0,l)
    return allsets
# auxilliary function for writing  and editing files 
def makedict(n):
    oldstr = []
    newstr = []
    m = pow(2,n)
    print m
    for i in range(m):
        if i <= 9:
           old = "x_"+str(i)+ " "
           oldstr.insert(0,old)
           new = "x_{"+str(i)+"}"
           newstr.insert(0,new)
        else:
           old = "x_"+str(i)
           oldstr.insert(0,old)
           new = "x_{"+str(i)+"}"
           newstr.insert(0,new)
       
    oldstr.insert(0,"<=")
    newstr.insert(0,"\leq")
    oldstr.insert(0,"union_closed_constraints:")
    newstr.insert(0," ")
    oldstr.insert(0,"fixed_family:")
    newstr.insert(0," ")
    mydict = zip(oldstr,newstr)
    a = dict((el,en) for (el,en) in mydict)
    print a
    return a
# auxilliary function for writing and editing files
def multiple_replace(dict, text):
  # Create a regular expression  from the dictionary keys
  regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

  # For each match, look-up corresponding value in dictionary
  return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) 

# auxilliary function for writing and editing files
def makelatex(n):
    with open("morriszero.ilp") as text:
         new_text = multiple_replace(makedict(n), text.read())
    with open("notes2.txt", "w") as result:
         result.write(new_text)
# auxilliary function for writing and editing files
def makedictbeam():
    oldstr = []
    newstr = []
    oldstr.insert(0,"&")
    newstr.insert(0,"\&")
    mydict = zip(oldstr,newstr)
    a = dict((el,en) for (el,en) in mydict)
    return a


# auxilliary function for writing and editing files
def makematrix():
    with open("change.txt") as text:
         new_text = multiple_replace(makedictbeam(), text.read())
    with open("beamermatrx.txt", "w") as result:
         result.write(new_text)           

    

# generating the integer weight vector, i.e., coefficients for WV inequality 
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
# make the objective function
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
# make coefficients
def makeccoff(r):
    l=[x for x in allsets()]
    makecoeff=[0]*6
    for i in range(len(r)):
        if r[i]==1.0:
           for j in range(0,6):       
               if l[i][j]==1:
                  makecoeff[j]=makecoeff[j]+1
    return makecoeff

def makeccoffint(r):
    l=[x for x in allsets()]
    makecoeff=[0]*6
    for i in range(len(r)):
        if r[i]==1.0:
           for j in range(0,6):       
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
                 
                  k=l.index([max(l[i][0],l[j][0]), max(l[i][1],l[j][1]), max(l[i][2],l[j][2]), max(l[i][3],l[j][3]), max(l[i][4],l[j][4]), max(l[i][5],l[j][5]), ])
                  if k!=j:
                    
                     constraintsf.append([j+1,k+1])
    return constraintsf

def constraints():
    l=[x for x in allsets()]
    constraints=[]
    for i in range(0,len(l)-1):
        for j in range(i+1, len(l)):
            k=l.index([max(l[i][0],l[j][0]), max(l[i][1],l[j][1]), max(l[i][2],l[j][2]), max(l[i][3],l[j][3]), max(l[i][4],l[j][4]), max(l[i][5],l[j][5]), ])
            if k != i:
               constraints.append([i+1,j+1,k+1])
    return constraints
# making list of uniform n-sets
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

# auxilliary function for writing and editing files
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
# auxilliary function for writing and editing files
def writingfunctionall(elist,listc):
     f = open("writematrix", "w")
     for i in range(len(elist)+1):
         if i==0:
            f.write(' \color{red}{W} & ')
         elif i < len(elist) and i >=1:
            d = i-1
            f.write(' \color{red}{%d} & ' %d)
         else:
            d = i-1
            f.write(' \color{red}{%d} \\\ \n' %d)
     for j in range(len(elist[0])):
         for i in range(len(elist)+1):
             if i==0:
                d=j+1
                f.write(str(listc[j]))
                f.write('& ')
             elif i < len(elist):
                k=i-1
                f.write(str(elist[k][j])+"& ")
             else:
                f.write(str(elist[k+1][j])+"\\\ \n")


# auxilliary function for writing and editing files
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
    fini = []
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
        final = [0]*len(p)
        for d in range(len(keep)):
            #print i
            if p[keep[d]][i]==1:
              # print 'here'
              # print p[keep[d]]
               final[keep[d]]=1
        for i in range(len(keep)):
             fina[keep[i]]=1
        fin.insert(0,fina)
        fini.insert(0,final) 
   
       
         
    return fin,fini
        
def scipfamily6generalconj(ll,fixer,hole):
    biggig =[]
    for g in range(len(ll)):
        l = [x for x in constraints()]
        p = [x for x in allsets()]
        weight=[1.0,1.0,-1.0]
        oweight=[1.0,-1.0]
        for i in range(len(l)):
            new=l[i] + weight
        c = [6,6,6,6,6,5]  
        cone = [0,100,41,39,40,27]  
        if fixer == 1:
           two = filtersets.zerone(ll[g])
        else:  
           two = ll[g]
        sets=two
        indexkeeps = filtersets.powerset(6)
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
        index = makesab(myfam,6)
        if hole == 0:
           index = index[0]
        if hole ==1:
           index = index[1]
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
                 #print 'hereererere'
                 keeperset=[]
                 for j in range(len(index[i])):
                     if index[i][j] >= 0.5:
                        keeperset.insert(0,j)
                # print count 
                # print [indexkeeps.index(p[x]) for x in keeperset]
                 cr=[x for x in makeccoff(index[i])]
                 print cr
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
                 #print size
                # print 'hereererere'
                 keeperset=[]
                 for j in range(len(index[i])):
                     if index[i][j] >= 0.5:
                        keeperset.insert(0,j)
                # print count 
                # print [indexkeeps.index(p[x]) for x in keeperset]
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
             print 'found what we need'
             slin.writeProblem('check.lp')
             break
          else:
              flag=0                       # otherwise we found a proof!
              print 'Found Infeasibility'
              slin.writeProblem('check.lp')
              #print nextguy  
             # print index 
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
             allguys = filtersets.powerset(6)
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

def scipfamily6general(lists):
    
    l = [x for x in constraints()]
    p = [x for x in allsets()]
    filterkeeper =[x for x in filtersets.getKoutMNsets(6,4,6)]
    indexkeeps = filtersets.powerset(6)
    onex = [0, 2, 4, 6, 7, 8, 10, 12, 14, 15, 16, 18, 20, 22, 23, 24, 26, 28, 30, 31, 32, 34, 36, 38, 39, 40, 42, 44, 46, 47, 48, 50, 51, 52, 54, 55, 56, 58, 59, 60, 62, 63]






    print onex


    two =   lists
          


    #print filterkeeper[0]
    # two=filterkeeper[455]
    #writingfunction(two)
   # return 0
    #print p[31]
    weight=[1.0,1.0,-1.0]
    oweight=[1.0,-1.0]
    for i in range(len(l)):
        new=l[i] + weight
    c = [6,6,6,6,6,5]  
    cone = [0,100,41,39,40,27]  
    #sets= filterkeeper[onex[1]]
    sets = two
    print sets
    allones=[1.0]*len(p)
    flag=1
    count=0
    index=[]
    fixf = Model()
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
              if i <=5:
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
              print onemore
              
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
          
         
          # optimize binary program
          # sbin.setMaximize()
          
          sbin.optimize()
          row=[None]*len(p)
          
         
          if sbin.getStatus()=="unknown" or sbin.getStatus()=="optimal":
             for j in range(len(p)):
                  row[j]=round(sbin.getVal(FranklVars[j]))
             index.insert(0,row)
          else:
             print 'We found the suckers!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'  # we found a proof!
             print c
             print [Fraction(x).limit_denominator() for x in c]
             sbin.writeProblem('checkIP.lp')
             print indexkeeps.index(p[20])
             flag = 0
          count=count+1
          sbin.free()
def scipfamily6generalmin(lists):
    biggig=[]
    finito = 0
    for g in range(len(lists)):
        two =[]
        for i in range(len(lists)):
            if i != g:
               two.insert(0,lists[i])
               
        print lists[g]
        print 'herehrereeeeeee'
        l = [x for x in constraints()]
        p = [x for x in allsets()]
        # one = [127, 125, 123, 121, 95, 93, 91, 89, 64, 61, 57, 32, 31, 29, 27, 25, 16, 8, 4, 2, 1, 0]
        #two= [p[x] for x in one]
        #writingfunction(two)
        #return 0
        #filterkeeper =[x for x in filtersets.getKoutMNsets(7,4,4)]
        weight=[1.0,1.0,-1.0]
        oweight=[1.0,-1.0]
        for i in range(len(l)):
            new=l[i] + weight
        c = [6,6,6,6,6,5,]  
        cone = [0,100,41,39,40,41]  
        sets = two
        indexkeeps = filtersets.powerset(6)
        print sets
        allones=[1.0]*len(p)
        allones=[1.0]*len(p)
        flag=1
        count=0
        index=[]
        fixf = Model()
        fixf.setMinimize()
        fixf.hideOutput()
    
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
        # [x for x in p if fixedfam[p.index(x)] > 0.0]
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
              if i <=6:
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
              finito = finito +1
              print g
              print g 
              print g
              slin.writeProblem('check.lp')
              
              for i in range(len(c)):
                  c[i]=slin.getVal(WeightVars[i])
              print c
             
             
              
         
          # add frankl variable
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
          
         
          # optimize binary program
          # sbin.setMaximize()
          
          sbin.optimize()
          row=[None]*len(p)
          
         
          if sbin.getStatus()=="unknown" or sbin.getStatus()=="optimal":
             for j in range(len(p)):
                  row[j]=round(sbin.getVal(FranklVars[j]))
             index.insert(0,row)
          else:
             print 'We found the suckers!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'  # we found a proof!
             print 'We found the suckers!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'  # we found a proof!
             print 'We found the suckers!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'  # we found a proof!
             print 'We found the suckers!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'  # we found a proof!
             print 'We found the suckers!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'  # we found a proof!
             print c
             print [Fraction(x).limit_denominator() for x in c]
             sbin.writeProblem('checkIP.lp')
             #print indexkeeps.index(p[20])
             #print g
             biggig.insert(0,g)
             flag = 0
          count=count+1
          sbin.free()
          
         
        
    print biggig
    print finito
           
             

              
             









