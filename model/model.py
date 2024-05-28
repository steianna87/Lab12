import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.countryList = DAO.getAllCountry()
        self.retailerList = None
        self.retailerMap = {}

        self.grafo = nx.Graph()

        self.solBest = []
        self.maxPeso = 0

    def CreaGrafo(self, country, year):
        self.grafo.clear()
        self.retailerList = DAO.getRetailer_by_country(country)
        for r in self.retailerList:
            self.retailerMap[r.Retailer_code] = r
        self.grafo.add_nodes_from(self.retailerList)

        for r1 in self.grafo.nodes:
            for r2 in self.grafo.nodes:
                if r1 != r2:
                    edge = DAO.getSpigolo(r1.Retailer_code, r2.Retailer_code, year, self.retailerMap)
                    if edge:
                        if self.grafo.has_edge(r1, r2):
                            self.grafo[r1][r2]['weight'] += edge[0].peso
                        else:
                            self.grafo.add_edge(r1, r2, weight=edge[0].peso)

    def calcola_volume(self):
        self.pesiRetailer = {}
        for r1 in self.grafo.nodes:
            for r2 in nx.neighbors(self.grafo, r1):
                try:
                    self.pesiRetailer[r1] += 0.5 * self.grafo[r1][r2]['weight']
                except KeyError:
                    self.pesiRetailer[r1] = 0.5 * self.grafo[r1][r2]['weight']
        print(self.pesiRetailer)
        return self.pesiRetailer

    def calcola_percorso(self, N):
        self.solBest = []
        self.maxPeso = 0

        for nodo in self.grafo.nodes:
            for vicino in nx.neighbors(self.grafo, nodo):
                self.ricorsione([nodo, vicino], N)

        print(f"soluzione trovata: {self.solBest}")

    def ricorsione(self, parziale, N):
        if len(parziale) > N + 1:
            return

        if parziale[0] == parziale[-1] and len(parziale) == N + 1:
            if self.getPeso(parziale) > self.maxPeso:
                self.maxPeso = self.getPeso(parziale)
                self.solBest = copy.deepcopy(parziale)
                print(f"{parziale} con peso: {self.maxPeso}")
                return

        ultimo = parziale[-1]
        for vicino in nx.neighbors(self.grafo, ultimo):
            if vicino not in parziale[1:] and vicino != parziale[0] or (len(parziale) == N):
                parziale.append(vicino)
                self.ricorsione(parziale, N)
                parziale.pop()

    def getPeso(self, parziale):
        peso = 0
        for i in range(len(parziale) - 1):
            peso += self.grafo[parziale[i]][parziale[i + 1]]['weight']
        return peso
