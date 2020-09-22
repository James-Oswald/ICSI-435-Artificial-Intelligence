
import numpy as np
from collections import deque

#undirected, unweighted graph G1

rawTest = {
    "S": ["a", "b", "d"],
    "a": ["S", "c"],
    "b": ["S", "d"],
    "c": ["a", "d", "e"],
    "d": ["b", "S", "c", "e"],
    "e": ["c", "d"]
}

#Note: The keys are sorted alphibetically, but the values are not sorted here, they are sorted later in adjList before being processed
rawG1 = {
    "S": ["d", "e", "p"],
    "a": ["b", "c"],
    "b": ["a", "d"],
    "c": ["a", "d", "f"],
    "d": ["S", "b", "c", "e"],
    "e": ["d", "S", "h", "r"],
    "f": ["c", "G", "r"],
    "h": ["p", "q", "e"],
    "p": ["S", "h", "q"],
    "q": ["p", "h"],
    "r": ["e", "f"],
    "G": ["f"]
}

rawG2 = {
    "S": ["d", "e", "p"],
    "a": [],
    "b": ["a"],
    "c": ["a"],
    "d": ["b", "c", "e"],
    "e": ["h", "r"],
    "f": ["c", "G"],
    "h": ["p", "q"],
    "p": ["q"],
    "q": [],
    "r": ["f"],
    "G": []
}

#letter to number for converting node labels to number
labels = ["S", "a", "b", "c", "d", "e", "f", "h", "p", "q", "r", "G"]
def l2n(l):
    return labels.index(l)
def n2l(n):
    return labels[n]

#convert the raw letter vertex list into a numeric vertex list
def adjList(rawGraph):
    rv = [None] * len(rawGraph)
    for nodeKey in rawGraph:
        rv[l2n(nodeKey)] = sorted([l2n(nodeLbl) for nodeLbl in rawGraph[nodeKey]])
    return rv

#convert the raw letter vertex list into a numeric adjacency matrix
def adjMat(rawGraph):
    aList = adjList(rawGraph)
    aMat = np.zeros((len(aList), len(aList)))
    for i in range(0, len(aList)):
        for elm in aList[i]:
            aMat[i, elm] = 1
    return aMat

def printData(data):
    if data == None:
        print("Goal node not found")
        return
    print("\tStates Expanded: " + str([n2l(e) for e in data[0]]))
    print("\tPath Returned:   " + str([n2l(e) for e in data[1]]))

#DFS stack implemnation using an adjacency matrix
def dfsStackMat(graph, start, end):
    stack = [start]
    expanded = []
    path = []
    pathDict = {}
    visited = [False for i in range(len(graph))]
    while len(stack) > 0:
        top = stack.pop()
        if not visited[top]:
            visited[top] = True
            expanded.append(top)
            if top == end:
                back = end          #path calculation
                while back != start:
                    path.append(back)
                    back = pathDict[back]
                path.append(start)
                return expanded, list(reversed(path))
            edges = [i for i in range(len(graph[top]) - 1, -1, -1) if graph[top, i] == 1]
            for connected in edges:
                if not visited[connected]:   #used for the path dict, not nesscary for the alg
                    stack.append(connected)
                    pathDict[connected] = top
    return None

#DFS stack implemnation using a vertex list
def dfsStackList(graph, start, end):
    stack = [start]
    expanded = []
    path = []
    pathDict = {}
    visited = [False for i in range(len(graph))]
    while len(stack) > 0:
        top = stack.pop()
        if not visited[top]:
            visited[top] = True
            expanded.append(top)
            if top == end:
                back = end              #path calculation
                while back != start:
                    path.append(back)
                    back = pathDict[back]
                path.append(start)
                return expanded, list(reversed(path))
            edges = list(reversed(graph[top]))
            for connected in edges:
                if not visited[connected]: #used for the path dict, not nesscary for the alg
                    stack.append(connected)
                    pathDict[connected] = top
    return None

#DFS recursive implemnation using an adjacency matrix
def dfsRecurMat(graph, start, end, visited = None, expanded = [], path = []):
    if visited == None:
        visited = [False for i in range(len(graph))]
        expanded = []
        path = []
    visited[start] = True
    expanded.append(start)
    path.append(start)
    if start == end:
        return expanded, path
    edges = [i for i in range(0, len(graph[start])) if graph[start, i] == 1]
    for connected in edges:
        if not visited[connected]:
            rv = dfsRecurMat(graph, connected, end, visited, expanded, path)
            if rv == None:
                path.pop()
            else:
                return rv
    return None

#DFS recursive implemnation using a vertex list
def dfsRecurList(graph, start, end, visited = None, expanded = [], path = []):
    if visited == None:
        visited = [False for i in range(len(graph))]
        expanded = []
        path = []
    visited[start] = True
    expanded.append(start)
    path.append(start)
    if start == end:
        return expanded, path
    edges = graph[start]
    for connected in edges:
        if not visited[connected]:
            rv = dfsRecurList(graph, connected, end, visited, expanded, path)
            if rv == None:
                path.pop()
            else:
                return rv
    return None

#BFS Queue Implementation using an adjacency matrix
def bfsQueueMat(graph, start, end):
    expanded = []
    path = []
    pathDict = {}
    visited = [False for i in range(len(graph))]
    visited[start] = True
    queue = deque()
    queue.append(start)
    while len(queue) > 0:
        front = queue.popleft()
        expanded.append(front)
        if front == end:
            back = end              #path calculation
            while back != start:
                path.append(back)
                back = pathDict[back]
            path.append(start)
            return expanded, list(reversed(path))
        edges = [i for i in range(0, len(graph[front])) if graph[front, i] == 1]
        for connected in edges:
            if not visited[connected]:
                visited[connected] = True
                pathDict[connected] = front
                queue.append(connected)
    return None


#BFS Queue Implementation using a vertex list
def bfsQueueList(graph, start, end):
    expanded = []
    path = []
    pathDict = {}
    visited = [False for i in range(len(graph))]
    visited[start] = True
    queue = deque()
    queue.append(start)
    while len(queue) > 0:
        front = queue.popleft()
        expanded.append(front)
        if front == end:
            back = end              #path calculation
            while back != start:
                path.append(back)
                back = pathDict[back]
            path.append(start)
            return expanded, list(reversed(path))
        edges = graph[front]
        for connected in edges:
            if not visited[connected]:
                visited[connected] = True
                pathDict[connected] = front
                queue.append(connected)
    return None


#BFS Recursive Implementation using a vertex list
def bfsRecurMat(graph, start, end, level = None, visited = None, expanded = [], pathDict = {}):
    if visited == None: #initialization
        visited = [False for i in range(len(graph))]
        visited[start] = True
        level = [start]
        expanded = []
        pathDict = {}
    if len(level) == 0: #Base case for failiure to find end
        return None
    nextLevel = []      #recursive case
    for node in level:
        expanded.append(node)
        if node == end:
            path = []
            back = end              #path calculation
            while back != start:
                path.append(back)
                back = pathDict[back]
            path.append(start)
            return expanded, list(reversed(path))
        edges = [i for i in range(0, len(graph[node])) if graph[node, i] == 1]
        for connected in edges:
            if not visited[connected]:
                visited[connected] = True
                nextLevel.append(connected)
                pathDict[connected] = node
    return bfsRecurMat(graph, start, end, nextLevel, visited, expanded, pathDict)

#BFS Recursive Implementation using a vertex list
def bfsRecurList(graph, start, end, level = None, visited = None, expanded = [], pathDict = {}):
    if visited == None: #initialization
        visited = [False for i in range(len(graph))]
        visited[start] = True
        level = [start]
        expanded = []
        pathDict = {}
    if len(level) == 0: #Base case for failiure to find end
        return None
    nextLevel = []      #recursive case
    for node in level:
        expanded.append(node)
        if node == end:
            path = []
            back = end              #path calculation
            while back != start:
                path.append(back)
                back = pathDict[back]
            path.append(start)
            return expanded, list(reversed(path))
        edges = graph[node]
        for connected in edges:
            if not visited[connected]:
                visited[connected] = True
                nextLevel.append(connected)
                pathDict[connected] = node
    return bfsRecurList(graph, start, end, nextLevel, visited, expanded, pathDict)



#printData(dfsStackMat(adjMat(rawTest), l2n("S"), l2n("e")))
#printData(dfsRecurMat(adjMat(rawTest), l2n("S"), l2n("e")))

printData(bfsQueueMat(adjMat(rawG1), l2n("S"), l2n("G")))
printData(bfsRecurList(adjList(rawG1), l2n("S"), l2n("G")))



print("P1) Perform DFS and BFS on unweighted graphs G1 and G2.")
print("Given the undirected graph G1 represented as vertex-list:")
print("Perform DFS using recursion. (1pt)")
printData(dfsRecurList(adjList(rawG1), l2n("S"), l2n("G")))
print("Perform DFS using stack. (1pt)")
printData(dfsStackList(adjList(rawG1), l2n("S"), l2n("G")))
print("Perform BFS using recursion. (1pt)")
printData(bfsRecurList(adjList(rawG1), l2n("S"), l2n("G")))
print("Perform BFS using stack. (1pt)")
printData(bfsQueueList(adjList(rawG1), l2n("S"), l2n("G")))
print("Given the undirected graph G1 represented as adjacency matrix:")
print("Perform DFS using recursion. (1pt)")
printData(dfsRecurMat(adjMat(rawG1), l2n("S"), l2n("G")))
print("Perform DFS using stack. (1pt)")
printData(dfsStackMat(adjMat(rawG1), l2n("S"), l2n("G")))
print("Perform BFS using recursion. (1pt)")
printData(bfsRecurMat(adjMat(rawG1), l2n("S"), l2n("G")))
print("Perform BFS using stack. (1pt)")
printData(bfsQueueMat(adjMat(rawG1), l2n("S"), l2n("G")))
print("Given the directed graph G2 represented as vertex-list:")
print("Perform DFS using recursion. (1pt)")
printData(dfsRecurList(adjList(rawG2), l2n("S"), l2n("G")))
print("Perform DFS using stack. (1pt)")
printData(dfsStackList(adjList(rawG2), l2n("S"), l2n("G")))
print("Perform BFS using recursion. (1pt)")
printData(bfsRecurList(adjList(rawG2), l2n("S"), l2n("G")))
print("Perform BFS using stack. (1pt)")
printData(bfsQueueList(adjList(rawG2), l2n("S"), l2n("G")))
print("Given the directed graph G2 represented as adjacency matrix:")
print("Perform DFS using recursion. (1pt)")
printData(dfsRecurMat(adjMat(rawG2), l2n("S"), l2n("G")))
print("Perform DFS using stack. (1pt)")
printData(dfsStackMat(adjMat(rawG2), l2n("S"), l2n("G")))
print("Perform BFS using recursion. (1pt)")
printData(bfsRecurMat(adjMat(rawG2), l2n("S"), l2n("G")))
print("Perform BFS using stack. (1pt)")
printData(bfsQueueMat(adjMat(rawG2), l2n("S"), l2n("G")))










#bfsStack(adjMat(rawG1), l2n("S"))