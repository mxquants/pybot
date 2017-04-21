

# %% Fibonacci function
def fibo(n,p=0,q=1,first=True):
    if first:
        print(p,q,sep='\n')
        first = False
    if n==0:
        return 1 
    print(p+q)
    p,q=q,p+q
    return fibo(n-1,p,q,first)


# %% 

