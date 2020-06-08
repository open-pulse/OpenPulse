from collections import defaultdict
# load = [('11013331', 'KAT'), 
#         ('9085267', 'NOT'), 
#         ('5238761', 'ETH'), 
#         ('5349618', 'ETH'), 
#         ('11788544', 'NOT'), 
#         ('962142', 'ETH'), 
#         ('7795297', 'ETH'), 
#         ('7341464', 'ETH'), 
#         ('9843236', 'KAT'), 
#         ('5594916', 'ETH'), 
#         ('1550003', 'ETH')]

load = [(1, 'pipe_1'),
        (2, 'pipe_1'),
        (3, 'pipe_2'),
        (6, 'pipe_1'),
        (5, 'pipe_2'),
        (4, 'pipe_3'),
        (7, 'pipe_3'),]

A = defaultdict(list)
# A={}
for v, k in load: 
    A[k].append(v)
B = [{'type':k, 'items':v} for k,v in A.items()]