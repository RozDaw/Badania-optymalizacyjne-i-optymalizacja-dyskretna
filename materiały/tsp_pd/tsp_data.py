#!/usr/bin/python3

def tsp_rand(size,seed):
    print("data:",size)
    for a in range(size):
        for b in range(size):
            seed = (seed*69069+1)&0xFFFFFFFF
            d = (seed%99+1)*(a!=b)
            print('{:2d}'.format(d),end=" " )
        print()
    print()    

for n in range(10,21):
    tsp_rand(n,n)