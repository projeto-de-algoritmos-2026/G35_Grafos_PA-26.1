import csv
import ast
import heapq

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

def dijkstra(grafo, origem_id, destino_id):
    nos_origem = [no for no in grafo.arestas if no.startswith(origem_id + "_")]
    nos_destino = [no for no in grafo.arestas if no.startswith(destino_id + "_")]

    if not nos_origem or not nos_destino:
        return {"erro": "Estação não encontrada"}
    
    distancias = {no: float('inf') for no in grafo.arestas}
    anteriores = {no: None for no in grafo.arestas}
    pq = []

    for no in nos_origem:
        distancias[no] = 0
        heapq.heappush(pq, (0, no))

    no_final_encontrado = None

    while pq:
        custo_atual, no_atual = heapq.heappop(pq)

        if no_atual in nos_destino:
            no_final_encontrado = no_atual
            break

        if custo_atual > distancias[no_atual]:
            continue

        for vizinho, peso_aresta in grafo.arestas[no_atual].items():
            novo_custo = custo_atual + peso_aresta

            if novo_custo < distancias[vizinho]:
                distancias[vizinho] = novo_custo
                anteriores[vizinho] = no_atual
                heapq.heappush(pq, (novo_custo, vizinho))

    if no_final_encontrado is None:
        return {"erro": "Nenhum caminho encontrado."}
    
    caminho_reverso = []
    atual = no_final_encontrado

    while atual is not None:
        caminho_reverso.append(atual)
        atual = anteriores[atual]

    caminho = caminho_reverso[::-1]
    qtd_baldeacoes = 0
    for i in range(len(caminho) - 1):
        estacao1 = caminho[i].split('_')[0]
        estacao2 = caminho[i+1].split('_')[0]
        if estacao1 == estacao2:
            qtd_baldeacoes += 1

    caminho_detalhado = [grafo.nos_dados[no] for no in caminho]

    return {
        "caminho": caminho,
        "caminho_detalhado": caminho_detalhado,
        "tempo_total": distancias[no_final_encontrado],
        "qtd_baldeacoes": qtd_baldeacoes
    }
