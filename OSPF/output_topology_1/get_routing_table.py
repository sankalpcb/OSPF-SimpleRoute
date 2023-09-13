import numpy as np
import sys

if len(sys.argv) > 1:
    n = int(sys.argv[1])
# if len(sys.argv) > 2:
#     l = int(sys.argv[2])
    
for i in range(n):
    outfile = "outfile_"+str(i)
    fd = open(outfile)
    lines = fd.readlines()
    fd.close()
    RT = lines[384:392]
    # print(RT)
    print("ROUTING TABLE for Node",str(i))
    print()
    for t in RT:
        print(t)
