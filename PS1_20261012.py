#!/usr/bin/env python
# coding: utf-8

# In[5]:


#PS1_1 definition
#True judgement prior, False judgement belongs to "else"
#so that when one element equals to another, it still make sense
def Print_values(a, b, c):
    if a > b :
        if b > c :
            print(a, b, c)
        else :
            if a > c :
                print(a, c, b)
            else :
                print(c, a, b)
    else:
        if b > c:
            if a > c :
                print(a, c, b)
            else :
                print(c, a, b)
        else:
            print(c, b, a)



# In[7]:


#PS1_1 report
a = float(input("please enter value a = "))
b = float(input("please enter value b = "))
c = float(input("please enter value c = "))
Print_values(a, b, c)


# In[62]:


#PS1_2 definition

def Matrix_multip(M1,M2):
    multi = np.full((5,5),0)
    #define an original result array with full values of 0
    for i in range(5):
        for j in range(5):
            number = 0
            for k in range(10):
                number = number + M1[i][k]*M2[k][j]
            multi[i][j] = number
    #for M1: i rows and k column; for M2: k rows and j column
    #for multi: o was replaced before next loop of "number = 0"
    print("the function result is: \n", multi)
    return multi



# In[64]:


#PS1_2 output
import numpy as np
#creat array in specific shape with random integer between 0-50(51 is not included)
M1 = np.random.randint(0,51,size = (5,10))
M2 = np.random.randint(0,51,size = (10,5))
print("M1: \n",M1)
print("M2: \n",M2)
multi = Matrix_multip(M1,M2)
result = M1 @ M2
print("the correct answer is: \n", result)
print("the authentication is: \n",np.array_equal(multi, M1 @ M2))
## the authentication function is informed by Codex


# In[1]:


#PS1_3 definition
def Pascal_triangle(k):
    row = [1]
        ##the first number is 1,
    ##so the calculation start with the second number
    for lines in range(2,k+1):
        new_row = [1]
        ##the last number should be 1
        ##so end with the one before it
        for i in range(1,lines-1):
            number = row[i-1] + row[i]
            new_row.append(number)
        new_row.append(1)
        ##to append the last number of new_row
        row = new_row
        ##loop to the next line

    print("the ", k,"^th line is:")            
    print(row)

    summary = 0    
    ##sequence start with 0
    for i in range(0,k):
        summary = summary + row[i]
    print("the summary of ", k,"^th line is", summary)      


# In[4]:


#PS1_3 report
k = int(input("Please enter k: "))    
Pascal_triangle(k)    
Pascal_triangle(100)
Pascal_triangle(200)  


# In[57]:


#PS1_4 definition
#for even number, the last step should be double
#for odd number, the last step should be plus
#during the moves, double step must be faster than plus 
def Least_moves(x):

    moves = 0
    while x > 1 :
        if x % 2 == 0:
            x = x // 2
            ##double // to maitain integer type
        else:
            x = x-1
        moves = moves + 1
    return moves


# In[61]:


#PS1_4 output
x = int(input("how much money you want to get(<100)?"))
result = Least_moves(x)
print("the least moves to", x ,"is ", result)


# In[73]:


#PS1_5.1  definition
def Find_expression(x):
    digits = "123456789"
    expression_list = ["1"]
    ##start with digit "1"
    choices = ["","+","-"]

    ##creat a list with all expressions
    for i in range(1,9):
        ## loop for each digit
        new_expression_list = []
        ##record each expression

        for expre in expression_list:
            ##"expre" means the currently stored expressions, e.g. 12+3 and 12-3 and 123
            for symbol in choices:
                newexpre = (expre + symbol + digits[i])
                ##this line can concatenate current expres with next digit
                new_expression_list.append(newexpre)

        expression_list =  new_expression_list

    #creat a dictionary with value calculated by all expressions
    solution = {}
    for expre in expression_list:
        value = eval(expre)
        ## eval() get the value of a string
        if value not in solution:
            solution[value] = []
        solution[value].append(expre)
        #sort the different expressions of same value
    ##Find all results of the target number
    results = solution.get(x,[])
    ##create a list "results" to stored the selected solutions
    if x not in solution:
        print("target number've got not solution, target number:", x)
    else:
        for expre in results:
            print(expre, "=", x)
    return results




# In[80]:


##PS1_5.1 output
x = int(input("please input a target number:"))

#Question: why would be a different output between these two lines?
results = Find_expression(x)
Find_expression(x)


# In[77]:


##PS1_5.2 ploting 
import matplotlib.pyplot as plt
Total_solutions = []
for i in range(1,101):
    results = solution.get(i,[])
    frequency = len(results)

    Total_solutions.append(frequency)
number = range(1,101)
plt.plot(number, Total_solutions)

# Add x and y labels
plt.xlabel("number")
plt.ylabel("Total_solutions")

# Add figure title
plt.title("Total_solutions for numbers range from 1 to 100")

# Show plot
plt.show


# In[ ]:




