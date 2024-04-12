from random import choice
from collections import Counter
import sys

def solvepart1():
    #read in data
    data = fileRead("input.txt")
    global edges
    edges = {}
    for row in data:
        p1, p2s = row.split(":")
        edges[p1] = ()
        for p in p2s.strip().split(" "):
            edges[p] = ()
    for row in data:
        p1, p2s = row.split(":")
        for p in p2s.strip().split(" "):
            edges[p1] = edges[p1] + (p,)
            edges[p] = edges[p] + (p1,)

    #find shortest paths between 1000 random points
    nodes = list(edges.keys())
    newEdges = []
    for i in range(0, 500):
        if i % 50 == 0:
            print(i)
        start = choice(nodes)
        end = choice(nodes)
        pointPath = shortestPathBFS(start, end)
        for j in range(len(pointPath)-1):
            newEdges.append((pointPath[j], pointPath[j+1]))

    #find 3 most frequent edges in those paths
    count = Counter(newEdges)
    sortedCount = sorted(count.items(), key = lambda item: item[1], reverse = True)
    foundEdges = []
    for pair, count in sortedCount[:6]:
        foundEdges.append(set(pair))
    cutsSet = []
    for pair in foundEdges:
        if pair not in cutsSet:
            cutsSet.append(pair)
    cuts = [tuple(cut) for cut in cutsSet]

    
    #cut 3 found edges out of graph
    side1start = cuts[0][0]
    side2start = cuts[0][1]
    for cutEdge in cuts:
        adjacentA = list(edges[cutEdge[0]])
        adjacentA.remove(cutEdge[1])
        edges[cutEdge[0]] = tuple(adjacentA)
        adjacentB = list(edges[cutEdge[1]])
        adjacentB.remove(cutEdge[0])
        edges[cutEdge[1]] = tuple(adjacentB)

    #find area of each half of graph
    area1 = findAreaOfGraph(side1start)
    area2 = findAreaOfGraph(side2start)
    print(area1, area2, area1 * area2)


# use a BFS to find the shortest path between 2 points on the graph and returns all connections in that path
def shortestPathBFS(start, goal):
    nodeQueue = [start]
    visitedNodes = [start]
    parents = {}
    node = ""
    while len(nodeQueue) > 0:
        node = nodeQueue.pop(0)
        if node == goal:
            break
        for newNode in edges[node]:
            if newNode not in visitedNodes:
                visitedNodes.append(newNode)
                parents[newNode] = node
                nodeQueue.append(newNode)
    curr = node
    path = []
    while curr != start:
        path = [curr] + path
        curr = parents[curr]
    path = [curr] + path
    return path

# uses a BFS to find the number of nodes in a graph
def findAreaOfGraph(start):
    nodeQueue = [start]
    visitedNodes = [start]
    node = ""
    sum = 0
    while len(nodeQueue) > 0:
        sum = sum + 1
        node = nodeQueue.pop(0)
        for newNode in edges[node]:
            if newNode not in visitedNodes:
                visitedNodes.append(newNode)
                nodeQueue.append(newNode)
    return sum

def fileRead(name):
    data = []
    f = open(name, "r")
    for line in f:
        data.append(line);
    return data

solvepart1()