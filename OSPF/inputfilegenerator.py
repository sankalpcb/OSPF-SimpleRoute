import numpy as np
import sys
import random

n = 4
l = 5
MAX_COST = 30
MIN_COST = 5
inputfile = "infile"
if len(sys.argv) > 1:
    n = int(sys.argv[1])
if len(sys.argv) > 2:
    l = int(sys.argv[2])
if len(sys.argv) > 3:
    inputfile = sys.argv[3]
if len(sys.argv) > 4:
    MIN_COST = int(sys.argv[4])
if len(sys.argv) > 5:
    MAX_COST = int(sys.argv[5])

def generate_links():
    links = []
    nodes =[0]
    for i in range(1,n):
        x = random.choice(nodes)
        Cmin = random.randint(MIN_COST,MAX_COST)
        Cmax = random.randint(Cmin,MAX_COST)
        links.append([i,x,Cmin,Cmax])
        nodes.append(i)
    while len(links) != l:
        i = random.choice(nodes)
        j = random.choice(nodes)
        if [i,j] in [i[:2] for i in links] or [j,i] in [i[:2] for i in links] or i==j:
            continue
        Cmin = random.randint(MIN_COST,MAX_COST)
        Cmax = random.randint(Cmin,MAX_COST)
        links.append([i,j,Cmin,Cmax])
    return links

fd = open(inputfile, 'w+')
links = generate_links()
fd.write(str(n)+" "+str(l)+"\n")
for i in range(len(links)):
    fd.write(str(links[i][0])+" "+str(links[i][1])+" "+str(links[i][2])+" "+str(links[i][3])+"\n")
fd.close()