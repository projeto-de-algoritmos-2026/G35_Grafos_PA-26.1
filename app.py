from flask import Flask, render_template, request, jsonify
from grafo import GrafoMetro, dijkstra

app = Flask(__name__)

grafo_tempo = GrafoMetro()
grafo_tempo.carregar_do_csv()
grafo_baldeacao = GrafoMetro()
grafo_baldeacao.carregar_do_csv(peso_baldeacao=1000)

@app.route('/')
def index():
    estacoes_unicas = {}
    for id_no, dados in grafo_tempo.nos_dados.items():
        id_base = id_no.split('_')[0]
        if id_base not in estacoes_unicas:
            estacoes_unicas[id_base] = dados['nome']

    lista_estacoes = [{"id": k, "nome": v} for k, v in estacoes_unicas.items()]
    lista_estacoes.sort(key=lambda x: x['nome'])

    return render_template('index.html', estacoes=lista_estacoes)

@app.route('/api/calcular', methods=['POST'])
def calcular_rota():
    dados_requisicao = request.get_json()

    origem = dados_requisicao.get('origem')
    destino = dados_requisicao.get('destino')
    criterio = dados_requisicao.get('criterio')
    grafo_escolhido = grafo_tempo if criterio == 'tempo' else grafo_baldeacao
    resultado = dijkstra(grafo_escolhido, origem, destino)

    if "erro" not in resultado and criterio == 'baldeacao':
        tempo_inflado = resultado['tempo_total']
        qtd_baldeacoes = resultado['qtd_baldeacoes']
        tempo_real = tempo_inflado - (qtd_baldeacoes * 1000) + (qtd_baldeacoes * 5)
        resultado['tempo_total'] = tempo_real

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)