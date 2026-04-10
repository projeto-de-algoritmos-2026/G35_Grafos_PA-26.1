import csv
import ast

class GrafoMetro:
    def __init__(self):
        self.nos_dados = {}
        self.arestas = {}

    def adicionar_no(self, id_no, nome, lat, lon, linha):
        self.nos_dados[id_no] = {'nome': nome, 'lat': float(lat), 'lon': float(lon), 'linha': linha}
        if id_no not in self.arestas:
            self.arestas[id_no] = {}

    def adicionar_aresta(self, origem, destino, peso):
        self.arestas[origem][destino] = peso
        self.arestas[destino][origem] = peso
    
    def carregar_do_csv(self, peso_viagem=2, peso_baldeacao=5):
        linhas_por_estacao = {}
        with open('data/metrosp_stations.csv', mode='r', encoding='utf-8') as f:
            leitor = csv.DictReader(f)
            for linha_csv in leitor:
                estacao_id = linha_csv['station']
                nome = linha_csv['name']
                lat = linha_csv['lat']
                lon = linha_csv['lon']

                linhas = ast.literal_eval(linha_csv['line'])
                linhas_por_estacao[estacao_id] = linhas

                nos_desta_estacao = []
                for linha in linhas:
                    id_no = f"{estacao_id}_{linha}"
                    self.adicionar_no(id_no, nome, lat, lon, linha)
                    nos_desta_estacao.append(id_no)

                if len(nos_desta_estacao) > 1:
                    for i in range(len(nos_desta_estacao)):
                        for j in range(i + 1, len(nos_desta_estacao)):
                            self.adicionar_aresta(nos_desta_estacao[i], nos_desta_estacao[j], peso_baldeacao)

        with open('data/metrosp_stations.csv', mode='r', encoding='utf-8') as f:
            leitor = csv.DictReader(f)
            for linha_csv in leitor:
                estacao_atual = linha_csv['station']
                linhas_atuais = linhas_por_estacao[estacao_atual]
                vizinhos = ast.literal_eval(linha_csv['neigh'])

                for vizinho in vizinhos:
                    linhas_vizinho = linhas_por_estacao[vizinho]
                    linhas_em_comum = set(linhas_atuais).intersection(set(linhas_vizinho))

                    for linha_comum in linhas_em_comum:
                        no_origem = f"{estacao_atual}_{linha_comum}"
                        no_destino = f"{vizinho}_{linha_comum}"
                        self.adicionar_aresta(no_origem, no_destino, peso_viagem)
                        