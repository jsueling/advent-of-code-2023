from collections import defaultdict, Counter
from math import prod

import networkx as nx

class UnionFind:

  def __init__(self, n):
    self.rank = [1] * n
    self.par = [i for i in range(n)]

  def findPar(self, v):
    while self.par[v] != self.par[self.par[v]]:
      self.par[v] = self.par[self.par[v]]
    return self.par[v]

  def union(self, v1, v2):

    p1, p2 = self.findPar(v1), self.findPar(v2)

    if p1 == p2:
      return 0

    if self.rank[p1] > self.rank[p2]:
      self.par[p2] = p1
      self.rank[p1] += self.rank[p2]
    else:
      self.par[p1] = p2
      self.rank[p2] += self.rank[p1]

    return 1

class Day25:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")
  
  def p1(self):

    edges = []

    wireMap = {}

    wireNumber = 0

    for line in self.input:

      node, neighbours = line.split(": ")

      if node not in wireMap:
        wireMap[node] = wireNumber
        wireNumber += 1

      for neighbour in neighbours.split():

        if neighbour not in wireMap:
          wireMap[neighbour] = wireNumber
          wireNumber += 1

        edges.append((wireMap[node], wireMap[neighbour]))

    def count_components(wires):

      n = len(wireMap)

      uf = UnionFind(n)

      for v1, v2 in edges:

        if (v1, v2) in wires or (v2, v1) in wires:
          continue
        
        n -= uf.union(v1, v2)

      if n == 2:
        print("p1", prod(Counter([uf.findPar(v) for v in uf.par]).values()))

    # Credits to hyper-neutrino: https://www.youtube.com/watch?v=S_rdenmcsm8

    g = nx.Graph()
    
    for line in self.input:
      node, neighbours = line.split(":")
      for nei in neighbours.strip().split():
        g.add_edge(node, nei)

    cut_wires = nx.minimum_edge_cut(g)

    cut_wires = set([(wireMap[node], wireMap[nei]) for node, nei in cut_wires])

    count_components(cut_wires)

    g.remove_edges_from(nx.minimum_edge_cut(g))

    a, b = nx.connected_components(g)

    print("p1", len(a) * len(b))

    # Credits to 4HbQ: https://old.reddit.com/r/adventofcode/comments/18qbsxs/2023_day_25_solutions/ketzp94/

    G = defaultdict(set)

    for line in self.input:
      u, *vs = line.replace(':','').split()
      for v in vs: G[u].add(v); G[v].add(u)

    S = set(G)

    count = lambda v: len(G[v]-S)

    while sum(map(count, S)) != 3:
      S.remove(max(S, key=count))

    print("p1", len(S) * len(set(G)-S))

d25 = Day25()
d25.p1()