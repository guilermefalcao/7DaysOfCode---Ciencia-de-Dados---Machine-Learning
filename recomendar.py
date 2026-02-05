"""
Script para gerar recomendações personalizadas de filmes
"""

import pandas as pd
import numpy as np
import joblib
import argparse
from pathlib import Path

MODEL_PATH = Path('models')

def carregar_modelo(nome_modelo='svd'):
    """Carrega modelo treinado e dados auxiliares"""
    modelo = joblib.load(MODEL_PATH / f'modelo_{nome_modelo}.pkl')
    dados = joblib.load(MODEL_PATH / 'dados_auxiliares.pkl')
    return modelo, dados

def recomendar_filmes(user_id, modelo, dados, n_recomendacoes=5):
    """Gera recomendações para um usuário"""
    
    movies = dados['movies']
    ratings = dados['ratings']
    user_item_matrix = dados['user_item_matrix']
    
    # Filmes já avaliados pelo usuário
    filmes_avaliados = ratings[ratings['user_id'] == user_id]['item_id'].values
    
    # Todos os filmes
    todos_filmes = movies['item_id'].values
    
    # Filmes não avaliados
    filmes_nao_avaliados = [f for f in todos_filmes if f not in filmes_avaliados]
    
    # Predições simples (baseado em popularidade)
    if 'item_means' in modelo:
        predicoes = []
        for item_id in filmes_nao_avaliados:
            pred = modelo['item_means'].get(item_id, modelo['global_mean'])
            predicoes.append((item_id, pred))
    else:
        # Usar média global
        global_mean = ratings['rating'].mean()
        predicoes = [(item_id, global_mean) for item_id in filmes_nao_avaliados]
    
    # Top N recomendações
    predicoes.sort(key=lambda x: x[1], reverse=True)
    top_n = predicoes[:n_recomendacoes]
    
    # Adicionar títulos
    recomendacoes = []
    for item_id, rating_pred in top_n:
        titulo = movies[movies['item_id'] == item_id]['title'].values[0]
        recomendacoes.append({
            'item_id': item_id,
            'titulo': titulo,
            'rating_predito': rating_pred
        })
    
    return recomendacoes

def main():
    parser = argparse.ArgumentParser(description='Gerar recomendações de filmes')
    parser.add_argument('--user_id', type=int, default=1, help='ID do usuário')
    parser.add_argument('--n_recomendacoes', type=int, default=5, help='Número de recomendações')
    parser.add_argument('--modelo', type=str, default='popularity', help='Nome do modelo')
    
    args = parser.parse_args()
    
    print(f"\n🎬 Gerando recomendações para usuário {args.user_id}...\n")
    
    modelo, dados = carregar_modelo(args.modelo)
    recomendacoes = recomendar_filmes(args.user_id, modelo, dados, args.n_recomendacoes)
    
    print(f"🎯 Top {args.n_recomendacoes} Recomendações:\n")
    for i, rec in enumerate(recomendacoes, 1):
        print(f"{i}. {rec['titulo']}")
        print(f"   Rating predito: ⭐ {rec['rating_predito']:.2f}\n")

if __name__ == "__main__":
    main()
