from copy import deepcopy
import networkx as nx
from database.DAO import DAO
from model.team import Team


class Model:
    def __init__(self):
        self._idMapTeams = dict()
        self._graph = nx.Graph()
        self._year = None
        self.heaviestPath = []
        self.highestCost = 0


    def getAllYears(self):
        return DAO.getAllYears()

    def getAllTeamsYear(self, year):
        self._year = year
        self._idMapTeams = dict()
        teams =  DAO.getAllTeamsYear(year)
        for team in teams:
            self._idMapTeams[team.ID] = team
        return teams

    def buildGraph(self):
        self._graph = nx.Graph()
        self._graph.add_nodes_from(self._idMapTeams.values())
        self._edges = DAO.getAllEdgesYear(self._year)
        for edge in self._edges:
            self._graph.add_edge(self._idMapTeams[edge['u']], self._idMapTeams[edge['v']], weight=edge['weight'])
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getTeamDetails(self, team):
        details = []
        for t in self._graph[team]:
            details.append((t, self._graph[team][t]['weight']))
        details.sort(key=lambda row: -row[1])
        return details

    def getHeaviestPath(self, start):
        self.heaviestPath = []
        self.highestCost = 0
        parziale = [start]
        for node in nx.neighbors(self._graph, start):
            parziale.append(node)
            self._ricorsione(parziale)
            parziale.pop()
        return self.heaviestPath, self.highestCost

    def _ricorsione(self, parziale):
        if newCosto := self._getCosto(parziale) > self.highestCost:
            self.highestCost = newCosto
            self.heaviestPath = deepcopy(parziale)
        for node in  nx.neighbors(self._graph, parziale[-1]):
            if node not in parziale and self._graph[parziale[-2]][parziale[-1]]['weight'] > self._graph[parziale[-1]][node]['weight']:
                parziale.append(node)
                self._ricorsione(parziale)
                parziale.pop()

    def _getCosto(self, parziale):
        costo = 0
        for i in range(len(parziale)-1):
            costo += self._graph[parziale[i]][parziale[i+1]]['weight']
        return costo