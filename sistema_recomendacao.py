"""
Sistema de Recomendação de Filmes - MovieLens 100k
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

DATA_PATH = Path('ml-100k')
MODEL_PATH = Path('models')
MODEL_PATH.mkdir(exist_ok=True)

class SistemaRecomendacao:
    
    def __init__(self):
        self.ratings = None
        self.movies = None
        self.train_data = None
        self.test_data = None
        self.user_item_matrix = None
        self.modelos = {}
        self.resultados = {}
        
    def carregar_dados(self):
        print("📂 Carregando dados...")
        
        self.ratings = pd.read_csv(DATA_PATH / 'u.data', sep='\t', 
                                   names=['user_id', 'item_id', 'rating', 'timestamp'])
        
        self.movies = pd.read_csv(DATA_PATH / 'u.item', sep='|', encoding='latin-1',
                                  names=['item_id', 'title', 'release_date', 'video_release_date', 'imdb_url'] + 
                                  [f'genre_{i}' for i in range(19)], usecols=['item_id', 'title'])
        
        print(f"✅ {len(self.ratings):,} avaliações carregadas")
        print(f"✅ {len(self.movies):,} filmes carregados\n")
        
    def preparar_dados(self):
        print("🔧 Preparando dados para treinamento...")
        
        # Dividir em treino e teste
        self.train_data, self.test_data = train_test_split(self.ratings, test_size=0.2, random_state=42)
        
        # Criar matriz usuário-item
        self.user_item_matrix = self.train_data.pivot_table(
            index='user_id', columns='item_id', values='rating'
        ).fillna(0)
        
        print(f"✅ Treino: {len(self.train_data):,} | Teste: {len(self.test_data):,}\n")
        
    def calcular_metricas(self, predictions, true_ratings):
        rmse = np.sqrt(mean_squared_error(true_ratings, predictions))
        mae = mean_absolute_error(true_ratings, predictions)
        return rmse, mae
    
    def recomendacao_aleatoria(self):
        print("🎲 Modelo 1: Recomendação Aleatória")
        
        predictions = np.random.uniform(1, 5, len(self.test_data))
        rmse, mae = self.calcular_metricas(predictions, self.test_data['rating'].values)
        
        self.modelos['random'] = {'type': 'random'}
        self.resultados['random'] = {'RMSE': rmse, 'MAE': mae}
        print(f"   RMSE: {rmse:.4f} | MAE: {mae:.4f}\n")
        
    def recomendacao_popularidade(self):
        print("⭐ Modelo 2: Recomendação por Popularidade")
        
        # Calcular rating médio por filme
        item_means = self.train_data.groupby('item_id')['rating'].mean()
        global_mean = self.train_data['rating'].mean()
        
        # Predizer usando média do item
        predictions = self.test_data['item_id'].map(item_means).fillna(global_mean).values
        rmse, mae = self.calcular_metricas(predictions, self.test_data['rating'].values)
        
        self.modelos['popularity'] = {'item_means': item_means, 'global_mean': global_mean}
        self.resultados['popularity'] = {'RMSE': rmse, 'MAE': mae}
        print(f"   RMSE: {rmse:.4f} | MAE: {mae:.4f}\n")
        
    def recomendacao_knn_user(self):
        print("👥 Modelo 3: KNN User-Based")
        
        # Similaridade entre usuários
        user_similarity = cosine_similarity(self.user_item_matrix)
        
        predictions = []
        for _, row in self.test_data.iterrows():
            user_id = row['user_id']
            item_id = row['item_id']
            
            if user_id in self.user_item_matrix.index and item_id in self.user_item_matrix.columns:
                user_idx = self.user_item_matrix.index.get_loc(user_id)
                similar_users = user_similarity[user_idx]
                
                # Ratings dos usuários similares para este item
                item_ratings = self.user_item_matrix[item_id].values
                weighted_sum = np.dot(similar_users, item_ratings)
                sim_sum = np.sum(np.abs(similar_users))
                
                pred = weighted_sum / sim_sum if sim_sum > 0 else self.train_data['rating'].mean()
                pred = np.clip(pred, 1, 5)
            else:
                pred = self.train_data['rating'].mean()
            
            predictions.append(pred)
        
        rmse, mae = self.calcular_metricas(predictions, self.test_data['rating'].values)
        self.modelos['knn_user'] = {'user_similarity': user_similarity}
        self.resultados['knn_user'] = {'RMSE': rmse, 'MAE': mae}
        print(f"   RMSE: {rmse:.4f} | MAE: {mae:.4f}\n")
        
    def recomendacao_knn_item(self):
        print("🎬 Modelo 4: KNN Item-Based")
        
        # Similaridade entre itens
        item_similarity = cosine_similarity(self.user_item_matrix.T)
        
        predictions = []
        for _, row in self.test_data.iterrows():
            user_id = row['user_id']
            item_id = row['item_id']
            
            if user_id in self.user_item_matrix.index and item_id in self.user_item_matrix.columns:
                item_idx = self.user_item_matrix.columns.get_loc(item_id)
                similar_items = item_similarity[item_idx]
                
                # Ratings do usuário para itens similares
                user_ratings = self.user_item_matrix.loc[user_id].values
                weighted_sum = np.dot(similar_items, user_ratings)
                sim_sum = np.sum(np.abs(similar_items))
                
                pred = weighted_sum / sim_sum if sim_sum > 0 else self.train_data['rating'].mean()
                pred = np.clip(pred, 1, 5)
            else:
                pred = self.train_data['rating'].mean()
            
            predictions.append(pred)
        
        rmse, mae = self.calcular_metricas(predictions, self.test_data['rating'].values)
        self.modelos['knn_item'] = {'item_similarity': item_similarity}
        self.resultados['knn_item'] = {'RMSE': rmse, 'MAE': mae}
        print(f"   RMSE: {rmse:.4f} | MAE: {mae:.4f}\n")
        
    def recomendacao_svd(self):
        print("🧮 Modelo 5: SVD")
        
        # Aplicar SVD
        svd = TruncatedSVD(n_components=50, random_state=42)
        user_factors = svd.fit_transform(self.user_item_matrix)
        item_factors = svd.components_.T
        
        predictions = []
        for _, row in self.test_data.iterrows():
            user_id = row['user_id']
            item_id = row['item_id']
            
            if user_id in self.user_item_matrix.index and item_id in self.user_item_matrix.columns:
                user_idx = self.user_item_matrix.index.get_loc(user_id)
                item_idx = self.user_item_matrix.columns.get_loc(item_id)
                
                pred = np.dot(user_factors[user_idx], item_factors[item_idx])
                pred = np.clip(pred, 1, 5)
            else:
                pred = self.train_data['rating'].mean()
            
            predictions.append(pred)
        
        rmse, mae = self.calcular_metricas(predictions, self.test_data['rating'].values)
        self.modelos['svd'] = {'svd': svd, 'user_factors': user_factors, 'item_factors': item_factors}
        self.resultados['svd'] = {'RMSE': rmse, 'MAE': mae}
        print(f"   RMSE: {rmse:.4f} | MAE: {mae:.4f}\n")
        
    def comparar_modelos(self):
        print("=" * 70)
        print("📊 COMPARAÇÃO DE MODELOS")
        print("=" * 70)
        
        df_resultados = pd.DataFrame(self.resultados).T.sort_values('RMSE')
        
        print("\nRanking por RMSE (menor é melhor):")
        print("-" * 70)
        for idx, (modelo, row) in enumerate(df_resultados.iterrows(), 1):
            print(f"{idx}. {modelo:20} | RMSE: {row['RMSE']:.4f} | MAE: {row['MAE']:.4f}")
        
        melhor_modelo = df_resultados.index[0]
        print(f"\n🏆 Melhor modelo: {melhor_modelo.upper()}")
        print("=" * 70)
        return melhor_modelo
        
    def salvar_modelo(self, nome_modelo):
        print(f"\n💾 Salvando modelo '{nome_modelo}'...")
        
        joblib.dump(self.modelos[nome_modelo], MODEL_PATH / f'modelo_{nome_modelo}.pkl')
        joblib.dump({
            'movies': self.movies, 
            'ratings': self.ratings,
            'user_item_matrix': self.user_item_matrix,
            'train_data': self.train_data
        }, MODEL_PATH / 'dados_auxiliares.pkl')
        
        print(f"✅ Modelo salvo em: {MODEL_PATH / f'modelo_{nome_modelo}.pkl'}")
        
    def treinar_todos(self):
        print("=" * 70)
        print("🚀 TREINAMENTO DE MODELOS DE RECOMENDAÇÃO")
        print("=" * 70)
        print()
        
        self.carregar_dados()
        self.preparar_dados()
        self.recomendacao_aleatoria()
        self.recomendacao_popularidade()
        self.recomendacao_knn_user()
        self.recomendacao_knn_item()
        self.recomendacao_svd()
        
        melhor_modelo = self.comparar_modelos()
        self.salvar_modelo(melhor_modelo)
        print("\n✅ Treinamento concluído!")

def main():
    sistema = SistemaRecomendacao()
    sistema.treinar_todos()

if __name__ == "__main__":
    main()
