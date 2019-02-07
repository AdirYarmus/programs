#The main function fits to the data in a valid input file a linear fit.
#It prints the paremeters of the linear fit, chi^2 and chi^2 squared reduced.
#It plots the data and the linear fit and saves the plot.
#If the input is invalid, it notifies of error appropriately and stops.
def fit_linear(filename):
    L=read_file(filename)
    #read_file reads the file named filename.
    #It returns a 2D list as a raw version of the data for further analysis.
    INFO=check_input(L)
    #check_input checks L to see if the data extracted from the file is valid.
    #If so, it gives a 2D list [x,dx,y,dy].
    #The 2D list has formation ready to be used for calculations.
    #Else, it prints error and returns None.
    if INFO==None:
        return
    #Stop if INFO=None, as it means the input was invalid.
    PARA=a_b_da_db(INFO)
    #a_b_da_db takes the information INFO that was extracted from the file.
    #It calculates the values of a,b,da,db.
    #It prints the calculated values and returns a list of them: [a,b,da,db]. 
    CHI2RED=chi_squared(INFO,PARA,True,True)
    #chi2 takes the information INFO and the calculated parameters PARA.
    #It calculates chi^2 and chi^2 reduced and prints them if 3rd arg=True.
    #It returns chi^2.
    #If 4th arg=True, it uses the fixed formula (2), else it uses formula (1).
    plot(L,INFO,PARA)
    #plot calculates the values of the linear fit f=ax+b.
    #The values of x,y and dy are in INFO and the values of a and b are in PARA.
    #It plots the information INFO and the linear fit to it.
    #It saves the plot as 'linear_fit' in format SVG.
    return

#search_best_parameter first gets information for calculations like linear_fit.
#Then it searches for the parameters a and b that minimizes chi^2.
#It plots the linear fit with these parameters and in the same plot, the data.
#It plots chi^2 v.s a for the value of b that was found.
#It saves the plots.
def search_best_parameter(filename):
    from matplotlib import pyplot
    L=read_file(filename)
    INFO=check_input(L)
    A=L.pop(-2)
    B=L.pop(-1)
    #make L like the one gets for the linear_fit.
    #Erase the 2 last rows in L and put them in variables A and B.
    for i in range(1,4):
        A[i]=float(A[i])
        B[i]=float(B[i])
    #turn the numbers in A and B from string form to floats. 
    PARA=[]
    val_a=[]
    chi2=chi_squared(INFO,[A[1],B[1]],False,False)
    #PARA will be the list [a,b,da,db],val_a a list of a's values.
    #chi2 is chi_squared.
    for k in range(0,1+int((A[2]-A[1])/A[3])):
        a=A[1]+k*A[3]
        val_a=val_a+[a]
        for j in range(0,1+int((B[2]-B[1])/B[3])):
            b=B[1]+j*B[3]
            if chi_squared(INFO,[a,b],False,False)<chi2:
                chi2=chi_squared(INFO,[a,b],False,False)
                PARA=[a,b]       
    #Go over all the values of a and b and find the ones for chi^2_min.
    N=len(INFO[0])-1
    #N is the number of values of x,y in the file.
    chi2red=chi2/(N-2)
    PARA=PARA+[abs(A[3]),abs(B[3])]
    #Calculate chi^2 reduced and da db
    print("a = {0} +- {1}".format(PARA[0],PARA[2]))
    print("b = {0} +- {1}".format(PARA[1],PARA[3]))
    print("chi2 =",chi2)
    print("chi2_reduced =",chi2red)
    #print [a,b,da,db] chi^2 and chi^2 reduced that were found. 
    plot(L,INFO,PARA)
    #plot the fitted function and the data.
    #save as 'linear_fit.svg'.
    val_chi2=[]
    for a in val_a:
        val_chi2=val_chi2+[chi_squared(INFO,[a,PARA[1]],False,False)]
    #create a list named val_chi2 of the values of chi^2 for each a's value.
    p=pyplot.plot(val_a,val_chi2,'b')
    xl=pyplot.xlabel('a')
    xl=pyplot.ylabel('chi2(a, b = {0:.1f})'.format(PARA[1]))
    pyplot.savefig('numeric_sampling.svg')
    #plot chi^2 v.s a for b that was found with the appropriate axes' titles.
    #save as 'numeric_sampling.svg'.
    return
 
#read_file returns a list L of lists.
#each list in L has the "words" in each line in the file + edition.
def read_file(filename):
    file=open(filename,'r')
    data=file.readlines()
    #creating a list named data of the lines in the file
    L=[]
    for i in range(0,len(data)):
        lh=[]
        data[i]=data[i].rstrip('\n')
        if 'x axis' not in data[i] and 'y axis' not in data[i]:
            data[i]=data[i].lower()
        lh=data[i].split()
        if lh!=[]:
            L.append(lh)
    #creating a list L of lists, each containing the "words" in each line in the file. 
    #the "words" are converted to lower case to get rid of uppercase, except the axes' titles.
    #The '\n' is gone. A wordless line is ignored.
    file.close()
    return L

#check_input checks the input for validity.
#If it is valid, it returns a list of lists [x,dx,y,dy].
#Each list has the variable's name as its first element and then its values.
#This function produces infomration ready for calculatios!!! 
def check_input(L):
    for i in range(0,len(L)):
        if L[i][1]!='axis:' and L[i][0] not in ['a','b'] and len(L[i])!=len(L[0]):
            print("Input file error: Data lists are not the same length.")
            return
    #Checking if the lengths of all rows are the same.
    #ignoring the rows below the table.
    #The columns are not of the same length iff the rows are not either. 
    #such input is invalid so a proper error notification is printed.
    #then the function stops.
    rows=True    
    if 'x' in L[0] and 'y' in L[0]:
        rows=False
    #checking if the input is in row form or column form. rows=False-column form.
    x=[]
    y=[]
    dx=[]
    dy=[]
    if rows==True:        
        for i in range(0,4):
            if L[i][0]=='x':
                x=L[i]
            elif L[i][0]=='dx':
                dx=L[i]
            elif L[i][0]=='y':
                y=L[i]
            elif L[i][0]=='dy':
                dy=L[i]
    else:
        for j in range(0,4):
            for i in range(0,len(L)):
                if L[i][1]=='axis:' or L[i][0] in ['a','b']:
                    continue
                if L[0][j]=='x':
                    x.append(L[i][j])
                elif L[0][j]=='y':
                    y.append(L[i][j])
                elif L[0][j]=='dx':
                    dx.append(L[i][j])
                elif L[0][j]=='dy':
                    dy.append(L[i][j])
    #If the input is in row form, just put the list starting with 'x' in x etc.
    #Else, column form, go over each column, ignore the lines below the table.
    #If the "word" is in a column starting with 'x' put it in x, etc.
    info=[x,dx,y,dy]
    for i in range(0,len(info)):
        for j in range(1,len(info[i])):
            info[i][j]=float(info[i][j])
            if i==1 or i==3:
                if info[i][j]<=0:
                    print("Input file error: Not all uncertainties are positive.")
                    return 
    #Turning all numbers that are in string form to floats.
    #Checking if dx or dy have nonpositive values.
    #In such case, it prints an error notification and stops the function.
    #Else, input is valid and it returns information ready for calculations.
    #The information is in the form of a 2D list [x,dx,y,dy]
    return info


#A function calculating a,b,da and db from info and prints them.
#The function returns a list of values: parameters=[a,b,da,db] 
def a_b_da_db(info):
    from math import sqrt
    xx=['xx']
    xy=['xy']
    dydy=['dy^2']    
    for i in range(1,len(info[0])):
        xx=xx+[info[0][i]**2]
        xy=xy+[info[0][i]*info[2][i]]
        dydy=dydy+[info[3][i]**2]
    #Create equivavlents of x,dx,y,dy in info=[x,dx,y,dy] for x^2,y^2 and dy^2.
    #First element is the name and then the values.
    def avg(z,dy2):
        n=0
        d=0
        for i in range(1,len(z)):
           n=n+z[i]/dy2[i]
           d=d+1/dy2[i]
        return n/d
    #avg calculates the weighted average of z's values.
    #The weights are calculated from dy2.
    a=(avg(xy,dydy)-avg(info[0],dydy)*avg(info[2],dydy))/(avg(xx,dydy)-avg(info[0],dydy)**2)
    b=avg(info[2],dydy)-a*avg(info[0],dydy)
    N=len(info[0])-1
    dada=avg(dydy,dydy)/(N*(avg(xx,dydy)-avg(info[0],dydy)**2))
    da=sqrt(dada)
    dbdb=dada*avg(xx,dydy)
    db=sqrt(dbdb)
    #Calculating a,b,da,db.
    print("a = {0} +- {1}".format(a,da))
    print("b = {0} +- {1}".format(b,db))
    #printing a,b,da,db
    parameters=[a,b,da,db]
    return parameters

#chi_squared calculates chi squared and chi squared reduced.
#The function prints chi squared and chi squared reduced if toprint=True.
#It returns the calculated value of chi squared.
#If fix=True, use the fixed formula (2), else use the unfixed one (1). 
def chi_squared(info,parameters,toprint,fix):
    a=parameters[0]
    b=parameters[1]
    N=len(info[0])-1
    #N is the number of x,y values in the input file.
    #'-1' as the first element of info[0]='x' not a value of x.
    chi2=0
    for i in range(1,len(info[0])):
        if fix==True:
            chi2=chi2+((info[2][i]-(a*info[0][i]+b))/info[3][i])**2
        else:
            chi2=chi2+(info[2][i]-(a*info[0][i]+b))**2/(info[3][i]**2+4*a**2*info[1][i]**2)
    #Calculating chi squared
    chi2red=chi2/(N-2)
    #Calculating chi squared reduced.
    if toprint==True:
        print("chi2 =",chi2)
        print("chi2_reduced =",chi2red)
    #if arg toprint=True print the calculated values of chi^2 and chi^2 reduced.
    return chi2

#From info and parameters, plot calculates the values of the fit function f.
#It plots f as red line, the data in info in blue dots with error bars.
#Both f and the data are plotted in the same plot.
#It inserts as axes' labels, the titles in the last rows of L from read_file.
#It saves the plot. 
def plot(L,info,parameters):
    from matplotlib import pyplot
    a=parameters[0]
    b=parameters[1]
    f=[]
    for i in range(1,len(info[0])):
        f=f+[a*info[0][i]+b]
    p1=pyplot.plot(info[0][1:],f,'r')
    #plot f
    xl=pyplot.xlabel(L[-2][2]+' '+L[-2][3])
    xl=pyplot.ylabel(L[-1][2]+' '+L[-1][3])
    #insert axes' labels
    p2=pyplot.errorbar(info[0][1:],info[2][1:],info[3][1:],info[1][1:],fmt='none',ecolor='b')
    #plot data as errorbars
    pyplot.savefig('linear_fit.svg')
    #save plot
    return 
    


