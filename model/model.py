import networkx as nx
from database.DAO import DAO
from model.team import Team


class Model:
    def __init__(self):
        self._idMapTeams = dict()
        self._graph = nx.Graph()
        self._year = None


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