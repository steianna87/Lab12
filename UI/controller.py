import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

        self.selected_Country = None

    def fillDD(self):
        coutries = self._model.countryList
        for country in coutries:
            self._view.ddcountry.options.append(ft.dropdown.Option(country))
        self._view.update_page()

    def handle_graph(self, e):
        self._view.btn_graph.disabled=True
        self._view.txt_result.controls.clear()
        self._view.update_page()
        country = self._view.ddcountry.value
        if country is None:
            self._view.create_alert('Inserire la Nazione')
            return
        year = self._view.ddyear.value
        if year is None:
            self._view.create_alert("Inserire l'anno")
            return

        self._model.getRetailers(country)
        self._model.CreaGrafo(int(year))

        self._view.txt_result.controls.append(ft.Text(f"Grafo con {len(self._model.grafo.nodes)} nodi "
                                                      f"e {len(self._model.grafo.edges)} spigoli"))
        self._view.btn_graph.disabled = False
        self._view.btn_path.disabled = False
        self._view.update_page()

    def handle_volume(self, e):
        self._view.txtOut2.controls.clear()

        volumi = self._model.calcola_volume()
        elenco = []
        for v in volumi:
            elenco.append((v, volumi[v]))
        elenco.sort(key=lambda x: x[1], reverse=True)
        for r in elenco:
            self._view.txtOut2.controls.append(ft.Text(f"{r[0]} --> {int(r[1])}"))
        self._view.update_page()

    def handle_path(self, e):
        self._view.txtOut3.controls.clear()
        try:
            N = int(self._view.txtN.value)
            if N < 2:
                self._view.create_alert('inserire un numero maggiore di 2')
                return
        except ValueError:
            self._view.create_alert('inserire un numero maggiore di 2')
            return

        self._model.calcola_percorso(N)
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {self._model.maxPeso}"))
        grafo = self._model.grafo
        soluzione = self._model.solBest
        for i in range(len(soluzione)-1):
            self._view.txtOut3.controls.append(ft.Text(f"{soluzione[i]} --> {soluzione[i+1]}: "
                                                       f"{grafo[soluzione[i]][soluzione[i+1]]['weight']}"))

        self._view.update_page()

