# Sistema de Recomendação de Filmes - MovieLens 100k

## 📋 Sobre o Projeto

Este projeto faz parte do #7DaysOfCode de Ciência de Dados e implementa um **Sistema de Recomendação de Filmes** utilizando o dataset clássico MovieLens 100k.

O objetivo é criar um sistema capaz de recomendar 5 filmes para usuários com base em comportamentos passados, similar ao que empresas como Netflix, Amazon Prime e Spotify utilizam.

## 🎯 Objetivo

Desenvolver e comparar diferentes abordagens de sistemas de recomendação:
- **Recomendação Aleatória**: baseline simples
- **Recomendação por Popularidade**: filmes mais avaliados/bem avaliados
- **Filtragem Colaborativa**: baseada em similaridade entre usuários ou itens
- **Modelos de Machine Learning**: SVD, KNN, etc.

## 📊 Dataset

O **MovieLens 100k** contém:
- 100.000 avaliações (ratings)
- 943 usuários
- 1.682 filmes
- Escala de avaliação: 1 a 5 estrelas

### Arquivos principais:
- `u.data`: avaliações (user_id, item_id, rating, timestamp)
- `u.item`: informações dos filmes (id, título, data lançamento, gêneros)
- `u.user`: informações dos usuários (id, idade, gênero, ocupação)

## 🛠️ Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo 1: Criar ambiente virtual (recomendado)

```bash
python -m venv venv
venv\Scripts\activate
```

### Passo 2: Instalar dependências

```bash
pip install -r requirements.txt
```

## 🚀 Como Executar

### 1. Exploração dos Dados
```bash
python exploracao_dados.py
```

### 2. Treinar Modelos de Recomendação
```bash
python sistema_recomendacao.py
```

### 3. Fazer Recomendações (CLI)
```bash
python recomendar.py --user_id 1 --n_recomendacoes 5
```

### 4. Iniciar API REST
```bash
python app.py
```
A API estará disponível em `http://localhost:5000`

## 🌐 API REST

### Endpoints Disponíveis:

#### GET `/`
Informações sobre a API

#### GET `/health`
Health check da API

#### POST `/recomendar`
Gera recomendações de filmes

**Body (JSON):**
```json
{
  "user_id": 1,
  "n_recomendacoes": 5
}
```

**Resposta:**
```json
{
  "user_id": 1,
  "n_recomendacoes": 5,
  "recomendacoes": [
    {
      "item_id": 123,
      "titulo": "Star Wars (1977)",
      "rating_predito": 4.5
    }
  ]
}
```

### Testar com Postman/Insomnia:
Veja o arquivo `TESTES_API.md` para exemplos detalhados

## 🐳 Docker

### Construir imagem:
```bash
docker build -t movie-recommender-api .
```

### Executar container:
```bash
docker run -p 5000:5000 movie-recommender-api
```

## 📁 Estrutura do Projeto

```
.
├── ml-100k/                    # Dataset MovieLens
├── models/                     # Modelos treinados salvos
├── exploracao_dados.py         # Análise exploratória
├── sistema_recomendacao.py     # Treinamento dos modelos
├── recomendar.py               # Script CLI para recomendações
├── app.py                      # API REST com Flask
├── Dockerfile                  # Containerização com Docker
├── requirements.txt            # Dependências do projeto
├── TESTES_API.md              # Guia de testes da API
└── README.md                   # Este arquivo
```

## 🧠 Abordagens Implementadas

### 1. Recomendação Aleatória
- **Vantagem**: Simples, diversificada
- **Desvantagem**: Não personalizada, baixa precisão

### 2. Recomendação por Popularidade ⭐
- **Vantagem**: Simples, funciona bem para novos usuários
- **Desvantagem**: Viés de popularidade, não personalizada
- **Resultado**: Melhor modelo (RMSE: 1.0210)

### 3. Filtragem Colaborativa (User-Based)
- **Vantagem**: Personalizada, considera preferências similares
- **Desvantagem**: Problema de cold start, escalabilidade

### 4. Filtragem Colaborativa (Item-Based)
- **Vantagem**: Mais escalável que user-based
- **Desvantagem**: Requer muitos dados de interação

### 5. SVD (Singular Value Decomposition)
- **Vantagem**: Captura padrões latentes, boa precisão
- **Desvantagem**: Mais complexo, requer mais processamento

## 📈 Métricas de Avaliação

- **RMSE** (Root Mean Square Error): erro médio das predições
- **MAE** (Mean Absolute Error): erro absoluto médio

## 💾 Serialização do Modelo

Os modelos treinados são salvos usando `joblib` na pasta `models/`

## 🏷️ Tags

`#7DaysOfCode` `#MachineLearning` `#DataScience` `#Python` `#RecommendationSystem` `#Flask` `#API` `#Docker`

## 👨💻 Autor

Projeto desenvolvido como parte do **#7DaysOfCode** de Ciência de Dados - Machine Learning
