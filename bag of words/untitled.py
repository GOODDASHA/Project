import numpy as np



x = np.array([[[ float('nan'),  1],
        [ 3,  4],
        [ 6,  7]],
       [[ 9, 10],
        [12, 13],
        [15, 16]],
       [[18, 19],
        [21, 22],
        [24, 25]]])

print x.reshape((18,1))
x = [ float('nan'),  1]
print sum(x)