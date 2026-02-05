"""
Exploração dos Dados - MovieLens 100k
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

DATA_PATH = Path('ml-100k')

def carregar_dados():
    ratings = pd.read_csv(DATA_PATH / 'u.data', sep='\t', names=['user_id', 'item_id', 'rating', 'timestamp'])
    movies = pd.read_csv(DATA_PATH / 'u.item', sep='|', encoding='latin-1', 
                         names=['item_id', 'title', 'release_date', 'video_release_date', 'imdb_url'] + 
                         [f'genre_{i}' for i in range(19)], usecols=range(24))
    users = pd.read_csv(DATA_PATH / 'u.user', sep='|', names=['user_id', 'age', 'gender', 'occupation', 'zip_code'])
    return ratings, movies, users

def analise_basica(ratings, movies, users):
    print("=" * 60)
    print("ANÁLISE EXPLORATÓRIA - MOVIELENS 100K")
    print("=" * 60)
    
    print("\n📊 ESTATÍSTICAS GERAIS")
    print(f"Total de avaliações: {len(ratings):,}")
    print(f"Total de usuários: {ratings['user_id'].nunique():,}")
    print(f"Total de filmes: {ratings['item_id'].nunique():,}")
    
    print("\n⭐ DISTRIBUIÇÃO DAS AVALIAÇÕES")
    print(ratings['rating'].value_counts().sort_index())
    print(f"\nMédia: {ratings['rating'].mean():.2f}")
    print(f"Mediana: {ratings['rating'].median():.2f}")
    
    print("\n👤 ESTATÍSTICAS DE USUÁRIOS")
    avaliacoes_por_usuario = ratings.groupby('user_id').size()
    print(f"Média de avaliações por usuário: {avaliacoes_por_usuario.mean():.2f}")
    print(f"Usuário mais ativo: {avaliacoes_por_usuario.max()} avaliações")
    
    print("\n🎬 ESTATÍSTICAS DE FILMES")
    avaliacoes_por_filme = ratings.groupby('item_id').size()
    print(f"Média de avaliações por filme: {avaliacoes_por_filme.mean():.2f}")
    print(f"Filme mais avaliado: {avaliacoes_por_filme.max()} avaliações")
    
    sparsity = 1 - (len(ratings) / (ratings['user_id'].nunique() * ratings['item_id'].nunique()))
    print(f"\n📉 Esparsidade da matriz: {sparsity:.2%}")

def top_filmes(ratings, movies, n=10):
    print("\n" + "=" * 60)
    print(f"🏆 TOP {n} FILMES MAIS AVALIADOS")
    print("=" * 60)
    
    filmes_populares = ratings.groupby('item_id').agg({'rating': ['count', 'mean']}).reset_index()
    filmes_populares.columns = ['item_id', 'num_avaliacoes', 'rating_medio']
    filmes_populares = filmes_populares.merge(movies[['item_id', 'title']], on='item_id')
    top = filmes_populares.nlargest(n, 'num_avaliacoes')
    
    for idx, row in top.iterrows():
        print(f"{row['title'][:50]:50} | {row['num_avaliacoes']:4.0f} avaliações | ⭐ {row['rating_medio']:.2f}")

def visualizacoes(ratings, movies):
    print("\n📈 Gerando visualizações...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    ratings['rating'].value_counts().sort_index().plot(kind='bar', ax=axes[0, 0], color='steelblue')
    axes[0, 0].set_title('Distribuição das Avaliações', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Rating')
    axes[0, 0].set_ylabel('Frequência')
    
    avaliacoes_usuario = ratings.groupby('user_id').size()
    axes[0, 1].hist(avaliacoes_usuario, bins=50, color='coral', edgecolor='black')
    axes[0, 1].set_title('Avaliações por Usuário', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Número de Avaliações')
    axes[0, 1].set_ylabel('Número de Usuários')
    
    avaliacoes_filme = ratings.groupby('item_id').size()
    axes[1, 0].hist(avaliacoes_filme, bins=50, color='lightgreen', edgecolor='black')
    axes[1, 0].set_title('Avaliações por Filme', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Número de Avaliações')
    axes[1, 0].set_ylabel('Número de Filmes')
    
    filme_stats = ratings.groupby('item_id').agg({'rating': ['mean', 'count']}).reset_index()
    filme_stats.columns = ['item_id', 'rating_medio', 'num_avaliacoes']
    filme_stats = filme_stats[filme_stats['num_avaliacoes'] >= 50]
    top_rated = filme_stats.nlargest(20, 'rating_medio').merge(movies[['item_id', 'title']], on='item_id')
    
    axes[1, 1].barh(range(len(top_rated)), top_rated['rating_medio'], color='gold')
    axes[1, 1].set_yticks(range(len(top_rated)))
    axes[1, 1].set_yticklabels([t[:30] for t in top_rated['title']], fontsize=8)
    axes[1, 1].set_xlabel('Rating Médio')
    axes[1, 1].set_title('Top 20 Filmes (min. 50 avaliações)', fontsize=14, fontweight='bold')
    axes[1, 1].invert_yaxis()
    
    plt.tight_layout()
    plt.savefig('analise_exploratoria.png', dpi=300, bbox_inches='tight')
    print("✅ Visualizações salvas em 'analise_exploratoria.png'")

def main():
    print("🎬 Carregando dados do MovieLens 100k...\n")
    ratings, movies, users = carregar_dados()
    analise_basica(ratings, movies, users)
    top_filmes(ratings, movies, n=15)
    visualizacoes(ratings, movies)
    print("\n✅ Análise exploratória concluída!")

if __name__ == "__main__":
    main()
