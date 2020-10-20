
import queue as Q

rawTest = {
    "S": {"h": 0, "con": {"a":2, "b":3, "d":5}},
    "a": {"h": 2, "con": {"S":2, "c":4}},
    "b": {"h": 5, "con": {"S":3, "d":4}},
    "c": {"h": 2, "con": {"a":4, "d":1, "e":2}},
    "d": {"h": 1, "con": {"b":4, "S":5, "c":1, "e":5}},
    "e": {"h": 0, "con": {"c":2, "d":5}}
}

rawGraph= {
    "S": {"h": 0, "con": {"d":3, "e":9, "p":1}},
    "a": {"h": 5, "con": {"b":2, "c":2}},
    "b": {"h": 7, "con": {"a":2, "d":1}},
    "c": {"h": 4, "con": {"a":2, "d":8, "f":3}},
    "d": {"h": 7, "con": {"S":3, "b":1, "c":8, "e":2}},
    "e": {"h": 5, "con": {"d":2, "S":9, "h":8, "r":2}},
    "f": {"h": 2, "con": {"c":3, "G":2, "r":2}},
    "h": {"h": 11, "con": {"p":4, "q":4, "e":8}},
    "p": {"h": 14, "con": {"S":1, "h":4, "q":15}},
    "q": {"h": 12, "con": {"p":15, "h":4}},
    "r": {"h": 3, "con": {"e":2, "f":2}},
    "G": {"h": 0, "con": {"f":2}}
}

def getPath(pathDict, start, end):
    path = []
    back = end    
    while back != start:    #path calculation from final node to fist node
        path.append(back)
        back = pathDict[back]
    path.append(start)
    return list(reversed(path))

def greedySearch(graph, start, end):
    expandable = [start]    #array of nodes that can be expended to
    expanded = []
    pathdict = {}
    while len(expandable) > 0:
        bestGuess = min(expandable, key=lambda k: graph[k]["h"])  #Pick the node with the best heueristic 
        expandable.remove(bestGuess)
        expanded.append(bestGuess)
        if bestGuess == end:
            return expanded, getPath(pathdict, start, end)
        connectedNodes = list(graph[bestGuess]["con"].keys())
        for connectedNode in connectedNodes:
            if connectedNode not in expanded and connectedNode not in expandable:
                pathdict[connectedNode] = bestGuess
                expandable.append(connectedNode)
    return None


print("Greedy Search:")
#print(greedySearch(rawTest, "S", "e"))
expandedG, pathG = greedySearch(rawGraph, "S", "G")
print("Expanded to: " + str(expandedG))
print("Path returned: " + str(pathG) + "\n")

def AStarSearch(graph, start, end):
    expandable = Q.PriorityQueue()
    expandable.put((0, start))
    g = {start: 0}
    expanded = []
    pathdict = {}
    while not expandable.empty():
        bestGuess = expandable.get()[1]
        expanded.append(bestGuess)
        if bestGuess == end:
            return expanded, getPath(pathdict, start, end)
        connectedNodes = list(graph[bestGuess]["con"].keys())
        for connectedNode in connectedNodes:
            tg = g[bestGuess] + graph[bestGuess]["con"][connectedNode]
            if connectedNode not in g or tg < g[connectedNode]:
                pathdict[connectedNode] = bestGuess
                g[connectedNode] = tg
                #if connectedNode not in expandable.queue:
                expandable.put((g[connectedNode] + graph[connectedNode]["h"], connectedNode))
    return None

print("A* Search:")
#print(AStarSearch(rawTest, "S", "e"))
expandedG, pathG = AStarSearch(rawGraph, "S", "G")
print("Expanded to: " + str(expandedG))
print("Path returned: " + str(pathG) + "\n")
