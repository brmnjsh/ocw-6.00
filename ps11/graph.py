# 6.00 Problem Set 11
#
# graph.py
#
# A set of data structures to represent graphs
#

class Node(object):
   def __init__(self, name):
       self.name = str(name)
   def getName(self):
       return self.name
   def __str__(self):
       return self.name
   def __repr__(self):
      return self.name
   def __eq__(self, other):
      return self.name == other.name
   def __ne__(self, other):
      return not self.__eq__(other)

class Edge(object):
   def __init__(self, src, dest):
       self.src = src
       self.dest = dest
   def getSource(self):
       return self.src
   def getDestination(self):
       return self.dest
   def __str__(self):
       return str(self.src) + '->' + str(self.dest)

class Digraph(object):
   """
   A directed graph
   """
   def __init__(self):
       self.nodes = set([])
       self.edges = {}
   def addNode(self, node):
       if node in self.nodes:
           raise ValueError('Duplicate node')
       else:
           self.nodes.add(node)
           self.edges[node] = []
   def addEdge(self, edge):
       src = edge.getSource()
       dest = edge.getDestination()
       if not(src in self.nodes and dest in self.nodes):
           raise ValueError('Node not in graph')
       self.edges[src].append(dest)
   def childrenOf(self, node):
       return self.edges[node]
   def hasNode(self, node):
       return node in self.nodes
   def __str__(self):
       res = ''
       for k in self.edges:
           for d in self.edges[k]:
               res = res + str(k) + '->' + str(d) + '\n'
       return res[:-1]

class WeightedEdge(Edge):
    def __init__(self, src, dest, totalWeight, outsideWeight):
        self.src = src
        self.dest = dest
        self.totalWeight = totalWeight
        self.outsideWeight = outsideWeight
    def getTotalWeight(self):
        return self.totalWeight
    def getOutsideWeight(self):
        return self.outsideWeight

class WeightedDigraph(Digraph):
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        totalWeight = edge.getTotalWeight()
        outsideWeight = edge.getOutsideWeight()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append({'destination': dest, 'totalWeight': totalWeight, 'outsideWeight': outsideWeight})
#    def getDistance(self, path):
#        print self.edges[path[0]]
