#!/usr/bin/python3

def kp_rand(size,seed):
    print("data:",size,size)
    for a in range(size):
        for b in range(2):
            seed = (seed*69069+1)&0xFFFFFFFF
            d = (seed%99+1)
            print('{:2d}'.format(d),end=" " )
        print()
    print()

for n in range(10,100):
    kp_rand(n*10,n*10)
