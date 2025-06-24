import flet as ft
import networkx as nx


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillddAnno(self):
        for year in self._model.getAllYears():
            self._view._ddAnno.options.append(ft.dropdown.Option(year, on_click=self.handleYearSelection))

    def handleYearSelection(self, e):
        year = e.control.key
        if not year:
            self._view.create_alert('Seleziona un anno!')
            return
        self._view._ddSquadra.options.clear()
        self._view._txtOutSquadre.controls.clear()
        teams = self._model.getAllTeamsYear(year)
        self._view._txtOutSquadre.controls.append(ft.Text(f'{len(teams)} squadre nel {year}:'))
        for team in teams:
            self._view._ddSquadra.options.append(ft.dropdown.Option(key=team.ID, text=f'{team.teamCode} - {team.name}',
                                                                    data=team,
                                                                    on_click=self._saveTeam))
            self._view._txtOutSquadre.controls.append(ft.Text(f'{team.teamCode} - {team.name}'))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()
        n, ed = self._model.buildGraph()
        self._view._txt_result.controls.append(ft.Text(f'Grafo creato con {n} nodi e {ed} archi.', color='green'))
        self._view.update_page()

    def handleDettagli(self, e):
        self._view._txt_result.controls.clear()
        team = self._team
        if not team:
            self._view.create_alert('Scegliere una squadra!')
        details = self._model.getTeamDetails(team)
        for item in details:
            self._view._txt_result.controls.append(ft.Text(f'{item[0]} - {item[1]}'))
        self._view.update_page()

    def handlePercorso(self, e):
        self._view._txt_result.controls.clear()
        team = self._team
        if not team:
            self._view.create_alert('Scegliere una squadra!')
        path, w = self._model.getHeaviestPath(team)
        self._view._txt_result.controls.append(ft.Text(f'Percorso trovato lungo {len(path)} con peso {w}:'))
        for node in path:
            self._view._txt_result.controls.append(ft.Text(node))
        self._view.update_page()

    def _saveTeam(self, e):
        self._team = e.control.data