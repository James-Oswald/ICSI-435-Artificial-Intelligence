
import numpy as np
from collections import deque

#letter to number for converting node labels to number
l2n = lambda l: ord(l)
#number to letter for converting node labels to number
n2l = lambda n: chr(n)


#BFS stack implemnation using an adjacency matrix
def bfsStack(graph, start):
    stack = [start]
    visited = (([False] * graph.shape[0])[start] := 1)
    while len(stack) > 0:
        stack[-1] 
