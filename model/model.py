import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.countryList = DAO.getAllCountry()
        self.retailerList = []
        self.retailerMap = {}

        self.grafo = nx.Graph()
        self.archi_gia_presi = set()
        self.pesiRetailer = {}

        self.solBest = []
        self.maxPeso = 0

    def getRetailers(self, country):
        self.retailerList.clear()
        self.retailerList = DAO.getRetailer_by_country(country)
        for r in self.retailerList:
            self.retailerMap[r.Retailer_code] = r

    def CreaGrafo(self, year):
        self.grafo.clear()
        self.archi_gia_presi = set()
        self.grafo.add_nodes_from(self.retailerList)

        for r1 in self.grafo.nodes:
            for r2 in self.grafo.nodes:
                if r1 != r2:
                    edge = DAO.getSpigolo(r1.Retailer_code, r2.Retailer_code, year, self.retailerMap)
                    if (r1, r2) in self.archi_gia_presi or (r2, r1) in self.archi_gia_presi:
                        if edge:
                            if self.grafo.has_edge(r1, r2):
                                self.grafo[r1][r2]['weight'] += edge[0].peso
                            else:
                                self.grafo.add_edge(r1, r2, weight=edge[0].peso)
                    else:
                        self.archi_gia_presi.add((r1, r2))
                        self.archi_gia_presi.add((r2, r1))


    def calcola_volume(self):
        self.pesiRetailer = {}
        for r1 in self.grafo.nodes:
            for r2 in nx.neighbors(self.grafo, r1):
                try:
                    self.pesiRetailer[r1] += self.grafo[r1][r2]['weight']
                except KeyError:
                    self.pesiRetailer[r1] = self.grafo[r1][r2]['weight']
        print(self.pesiRetailer)
        return self.pesiRetailer

    def calcola_percorso(self, N):
        self.solBest = []
        self.maxPeso = 0

        for nodo in self.grafo.nodes:
            for vicino in nx.neighbors(self.grafo, nodo):
                self.ricorsione([nodo, vicino], N)

        print(f"Soluzione trovata: {self.solBest}")

    def ricorsione(self, parziale, N):
        if len(parziale) >= N + 1:
            return

        ultimo = parziale[-1]

        if len(parziale) == N:
            for vicino in nx.neighbors(self.grafo, ultimo):
                if vicino == parziale[0]:
                    parziale.append(vicino)
            if len(parziale) == N+1:
                if self.getPeso(parziale) > self.maxPeso:
                    self.maxPeso = self.getPeso(parziale)
                    self.solBest = copy.deepcopy(parziale)
                    print(f"{parziale} con peso: {self.maxPeso}")
                parziale.pop()
            return

        for vicino in nx.neighbors(self.grafo, ultimo):
            if vicino not in parziale:
                parziale.append(vicino)
                self.ricorsione(parziale, N)
                parziale.pop()

    def getPeso(self, parziale):
        peso = 0
        for i in range(len(parziale) - 1):
            peso += self.grafo[parziale[i]][parziale[i + 1]]['weight']
        return peso
