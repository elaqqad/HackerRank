'''
This algorithm is based on the paper (theorem 1):
http://www.dms.umontreal.ca/%7Eandrew/PDF/BinCoeff.pdf

Note that the cited version contains some errors ( mainly in theorem 1 
the definition of ej is not correct, I used the expression in the proof in 
section 3 instead)

Note also that this algorithm only uses the theorem 1 and NOT the algorithm
described in the section 3, so this can maybe improved.

----
Binomial(n,m) modulo Big
The method described here consists of :
-> decompose Big as product of powers of primes
-> for each power compute Binomial(n,m) modulo p^q using Theorem 1
-------> Compute the sequences ni,mi,ri,Ni,Mi,Ri and the integers e0 and e(q-1) named "eq"
-------> Compute the produt of all Ni as numerator
-------> Compute the produt of all Ri*Mi as denomerator
-------> use the formula (-1)^e0*p^eq*numerator*inverse(denomerator,p^q)
-> Use chainse remainder theorem to deduce the value of Binomial(n,m) modulo Big

>>> The complexity of this algorithm is O(log^2(n)) assuming that
the decomposition to product of primes is done in constant time.

>>> If the modulo has less than 100 digits then it can be factorized 
usign today's computers and sophisticated algorithms

----

El-aqqad mohamed
'''
globalFacts=dict()

# computes C(n,m) Modulo Big
def compute(n,m,big):
    y=decompose(big)
    remainders=[]
    for powerPrime in y:
        remainders.append(binomialModulo(n,m,powerPrime[0],powerPrime[1]))
    sol=chaineseRemainderTheorem([pow(i[0],i[1]) for i in y],remainders)
    return sol

# Retruns the solution to the chinese remainder system 
def chaineseRemainderTheorem(num,rem):
    prod = 1
    for i in num:
        prod *=i
    result = 0
    for i in range(len(num)):
        pp = prod // num[i]
        result += rem[i] * inverse(pp, num[i]) * pp;
    return result%prod

# Extended ecludien algorithm to compote gcd and inverse
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

# Compute a^(-1) modulo m
def inverse(a, m):
    g, x, y = egcd(a, m)
    return x % m

# Computes C(n,m) Modulo prime^(powerPrime) 
def binomialModulo(n,m,prime,powerPrime):
    power=int(pow(prime,powerPrime))
    nArray,mArray,rArray,NArray,MArray,RArray,e0,eq=allAtOnce(n,m,prime,powerPrime)
    result=1
    denominator=1
    result=pow(-1,eq)*pow(prime,e0)%power
    if(result==0):
        return 0
    for i in range(len(nArray)):
        result*=fact(NArray[i],prime,powerPrime)
        denominator*=fact(MArray[i],prime,powerPrime)*fact(RArray[i],prime,powerPrime)
        result=result%power
        denominator=denominator%power
    result*=inverse(denominator%power,power)
    return result%power

# Compute (k!)_prime modulo prime^(powerPrime) 
def fact(k,prime,powerPrime):
    power=pow(prime,powerPrime)
    if( (k,power) in globalFacts ):
        return globalFacts[(k,power)]
    factorial=1
    for i in range(1,k+1):
        if(i%prime != 0):
            factorial=(factorial*i)%power
    globalFacts[(k,power)]=factorial
    return factorial

# Compute the representation of the integers n and m and r-m in base p
# Compute e0, eq=e_{q-1}
# For details, refer to the cited paper above
def allAtOnce(n,m,prime,powerPrime):
    nArray=[]
    mArray=[]
    rArray=[]
    NArray=[]
    MArray=[]
    RArray=[]
    r=n-m
    e0=0
    eq=0
    j=0
    power=int(pow(prime,powerPrime))
    while(n>0):
        nArray.append((n%prime))
        mArray.append((m%prime))
        rArray.append((r%prime))
        NArray.append((n%power))
        MArray.append((m%power))
        RArray.append((r%power))
        n=n//prime
        r=r//prime
        m=m//prime
        j=j+1
        if(n!=m+r):
            e0=e0+1
            if(j>=powerPrime):
                eq=eq+1
    return nArray,mArray,rArray,NArray,MArray,RArray,e0,eq

def decompose(big):
    # Todo write a decomposition algorithm in prime factors
    return [(11,1),(13,1),(37,1),(3,3)]

# The main program
t= int(input().strip())

for i in range(t):
    arr = [int(arr_temp) for arr_temp in input().strip().split(' ')]
    n=arr[0]
    m=arr[1]
    # Now compute nCm modulo 142857
    result=compute(n,m,14857)
    # print the result
    print(result)
