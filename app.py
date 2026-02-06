"""
API REST para Sistema de Recomendação de Filmes
Serve o modelo de Machine Learning através de endpoints HTTP
"""

from flask import Flask, request, jsonify
import joblib
import pandas as pd
from pathlib import Path

# Inicializar Flask
app = Flask(__name__)

# Caminhos
MODEL_PATH = Path('models')

# Carregar modelo e dados na inicialização (para melhor performance)
print("🔄 Carregando modelo e dados...")
modelo = joblib.load(MODEL_PATH / 'modelo_popularity.pkl')
dados = joblib.load(MODEL_PATH / 'dados_auxiliares.pkl')
print("✅ Modelo carregado com sucesso!")


def gerar_recomendacoes(user_id, n_recomendacoes=5):
    """
    Gera recomendações de filmes para um usuário
    
    Args:
        user_id (int): ID do usuário
        n_recomendacoes (int): Número de recomendações a retornar
    
    Returns:
        list: Lista de dicionários com recomendações
    """
    movies = dados['movies']
    ratings = dados['ratings']
    
    # Filmes já avaliados pelo usuário
    filmes_avaliados = ratings[ratings['user_id'] == user_id]['item_id'].values
    
    # Todos os filmes disponíveis
    todos_filmes = movies['item_id'].values
    
    # Filmes não avaliados (candidatos para recomendação)
    filmes_nao_avaliados = [f for f in todos_filmes if f not in filmes_avaliados]
    
    # Gerar predições usando o modelo
    if 'item_means' in modelo:
        predicoes = []
        for item_id in filmes_nao_avaliados:
            pred = modelo['item_means'].get(item_id, modelo['global_mean'])
            predicoes.append((item_id, pred))
    else:
        global_mean = ratings['rating'].mean()
        predicoes = [(item_id, global_mean) for item_id in filmes_nao_avaliados]
    
    # Ordenar por rating predito (maior para menor)
    predicoes.sort(key=lambda x: x[1], reverse=True)
    top_n = predicoes[:n_recomendacoes]
    
    # Montar resposta com títulos dos filmes
    recomendacoes = []
    for item_id, rating_pred in top_n:
        titulo = movies[movies['item_id'] == item_id]['title'].values[0]
        recomendacoes.append({
            'item_id': int(item_id),
            'titulo': titulo,
            'rating_predito': float(rating_pred)
        })
    
    return recomendacoes


@app.route('/', methods=['GET'])
def home():
    """
    Endpoint raiz - Informações sobre a API
    """
    return jsonify({
        'mensagem': 'API de Recomendação de Filmes - MovieLens 100k',
        'versao': '1.0',
        'endpoints': {
            '/': 'GET - Informações da API',
            '/recomendar': 'POST - Gerar recomendações de filmes',
            '/health': 'GET - Status da API'
        },
        'exemplo_uso': {
            'url': '/recomendar',
            'metodo': 'POST',
            'body': {
                'user_id': 1,
                'n_recomendacoes': 5
            }
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """
    Endpoint de health check - Verifica se a API está funcionando
    """
    return jsonify({
        'status': 'OK',
        'modelo_carregado': True,
        'mensagem': 'API funcionando corretamente'
    }), 200


@app.route('/recomendar', methods=['POST'])
def recomendar():
    """
    Endpoint principal - Gera recomendações de filmes
    
    Espera JSON no body:
    {
        "user_id": 1,
        "n_recomendacoes": 5
    }
    
    Retorna JSON com recomendações:
    {
        "user_id": 1,
        "n_recomendacoes": 5,
        "recomendacoes": [...]
    }
    """
    try:
        # Validar se a requisição é JSON
        if not request.is_json:
            return jsonify({
                'erro': 'Content-Type deve ser application/json'
            }), 400
        
        # Obter dados da requisição
        data = request.get_json()
        
        # Validar campos obrigatórios
        if 'user_id' not in data:
            return jsonify({
                'erro': 'Campo "user_id" é obrigatório'
            }), 400
        
        # Extrair parâmetros
        user_id = data['user_id']
        n_recomendacoes = data.get('n_recomendacoes', 5)  # Default: 5
        
        # Validar tipos
        if not isinstance(user_id, int):
            return jsonify({
                'erro': 'Campo "user_id" deve ser um número inteiro'
            }), 400
        
        if not isinstance(n_recomendacoes, int):
            return jsonify({
                'erro': 'Campo "n_recomendacoes" deve ser um número inteiro'
            }), 400
        
        # Validar valores
        if user_id < 1 or user_id > 943:
            return jsonify({
                'erro': 'user_id deve estar entre 1 e 943'
            }), 400
        
        if n_recomendacoes < 1 or n_recomendacoes > 50:
            return jsonify({
                'erro': 'n_recomendacoes deve estar entre 1 e 50'
            }), 400
        
        # Gerar recomendações
        recomendacoes = gerar_recomendacoes(user_id, n_recomendacoes)
        
        # Retornar resposta
        return jsonify({
            'user_id': user_id,
            'n_recomendacoes': n_recomendacoes,
            'total_recomendacoes': len(recomendacoes),
            'recomendacoes': recomendacoes
        }), 200
    
    except Exception as e:
        return jsonify({
            'erro': 'Erro interno do servidor',
            'detalhes': str(e)
        }), 500


if __name__ == '__main__':
    # Rodar servidor Flask
    # debug=True: recarrega automaticamente ao modificar código
    # host='0.0.0.0': permite acesso externo
    # port=5000: porta padrão do Flask
    app.run(debug=True, host='0.0.0.0', port=5000)
