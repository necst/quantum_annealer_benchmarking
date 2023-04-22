import json
import string
import random as random


def generate_random_string():
   """
   In this method a random dictionary is created, the first element is a name,
   the second one is a weight"
   """
   S = random.randint(1,4)  # number of characters in the string.  
   # call random.choices() string module to find the string in Uppercase + numeric data.  
   ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
   return str(ran)

def new_dict_with_weight(string):   
    return dict(name=string,weight=random.randint(1,10))

def new_dict_without_weight(string):
    return dict(name=string)
      
def new_cons(array,dim): 
    m = random.randint(2,dim)
    var = set()
    while len(var) < m:
        var.add(array[random.randint(0,len(array)-1)])
    return dict(sets = list(var))
 

def generate(filename, n: int):
    """
    This method generates a new random instance of Set Packing Problem, for a given size n, and writes it into a file, according to the presented format.
    """
    
    assert n > 0
    
    s = set()
    while len(s) < n:
        s.add(generate_random_string())
    s = list(s)
    """
    We have to declare a list of n dictionaries in order to parse it in a
    json array of objects
    """

    sub = []
    for i in range(1, n + 1):
        if random.randint(0,1) == 1:
            sub.append(new_dict_without_weight(s[i-1]))
        else:
            sub.append(new_dict_with_weight(s[i-1]))
            
        
    cons = []
    num = random.randint(1, n)
    for j in range(1,num):
        cons.append(new_cons(s,n))

    problem = []
    problem.append(dict(subsets=sub,constraints=cons))

    with open(filename, "w") as outfile:
        json.dump(problem, outfile)
    












