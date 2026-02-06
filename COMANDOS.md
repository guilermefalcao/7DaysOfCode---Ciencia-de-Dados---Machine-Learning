# 🚀 Guia de Comandos - API de Recomendação

## 📦 Instalação

```bash
# 1. Ativar ambiente virtual
cd "C:\1. Guilherme\00. Dataprev\0000. projeto conta\cursoSpringboot\7DaysOfCode - Ciência de Dados - Machine Learning"
venv\Scripts\activate

# 2. Instalar Flask (se ainda não instalou)
pip install flask

# Ou reinstalar todas as dependências
pip install -r requirements.txt
```

## 🎬 Executar a API

```bash
# Iniciar servidor Flask
python app.py
```

**Saída esperada:**
```
🔄 Carregando modelo e dados...
✅ Modelo carregado com sucesso!
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
```

A API estará rodando em: `http://localhost:5000`

## 🧪 Testar no Postman/Insomnia

### Teste 1: Health Check
- **Método:** GET
- **URL:** `http://localhost:5000/health`
- **Headers:** Nenhum
- **Resultado:** Status 200 OK

### Teste 2: Gerar Recomendações
- **Método:** POST
- **URL:** `http://localhost:5000/recomendar`
- **Headers:** 
  - `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "user_id": 1,
  "n_recomendacoes": 5
}
```
- **Resultado:** Lista de 5 filmes recomendados

### Teste 3: Diferentes usuários
```json
{
  "user_id": 50,
  "n_recomendacoes": 10
}
```

## 🐳 Docker (Opcional)

```bash
# Construir imagem
docker build -t movie-api .

# Executar container
docker run -p 5000:5000 movie-api
```

## 🛑 Parar a API

No terminal onde a API está rodando:
- Pressione `Ctrl + C`

## 📝 Comandos Git para subir no GitHub

```bash
# Adicionar novos arquivos
git add .

# Commit com hashtag #7DaysOfCode
git commit -m "feat: API REST com Flask para servir modelo de recomendação

- Endpoint POST /recomendar para gerar recomendações
- Validações de entrada (user_id, n_recomendacoes)
- Health check endpoint
- Dockerfile para containerização
- Documentação de testes com Postman

#7DaysOfCode #MachineLearning #API #Flask"

# Push para GitHub
git push origin main
```

## 🔍 Verificar se está funcionando

Abra o navegador e acesse:
- `http://localhost:5000/` - Informações da API
- `http://localhost:5000/health` - Health check
