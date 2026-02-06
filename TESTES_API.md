# 🧪 Guia de Testes da API - Postman/Insomnia

## 📋 Pré-requisitos
- API rodando em `http://localhost:5000`
- Postman ou Insomnia instalado

---

## 🔍 Teste 1: Health Check (GET)

**Endpoint:** `GET http://localhost:5000/health`

**Headers:** Nenhum necessário

**Resposta esperada:**
```json
{
  "status": "OK",
  "modelo_carregado": true,
  "mensagem": "API funcionando corretamente"
}
```

---

## 🏠 Teste 2: Informações da API (GET)

**Endpoint:** `GET http://localhost:5000/`

**Headers:** Nenhum necessário

**Resposta esperada:**
```json
{
  "mensagem": "API de Recomendação de Filmes - MovieLens 100k",
  "versao": "1.0",
  "endpoints": {...}
}
```

---

## 🎬 Teste 3: Gerar Recomendações (POST)

**Endpoint:** `POST http://localhost:5000/recomendar`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "user_id": 1,
  "n_recomendacoes": 5
}
```

**Resposta esperada:**
```json
{
  "user_id": 1,
  "n_recomendacoes": 5,
  "total_recomendacoes": 5,
  "recomendacoes": [
    {
      "item_id": 123,
      "titulo": "Star Wars (1977)",
      "rating_predito": 4.5
    },
    ...
  ]
}
```

---

## ❌ Teste 4: Validação - user_id ausente

**Endpoint:** `POST http://localhost:5000/recomendar`

**Body (JSON):**
```json
{
  "n_recomendacoes": 5
}
```

**Resposta esperada:**
```json
{
  "erro": "Campo \"user_id\" é obrigatório"
}
```
**Status Code:** 400

---

## ❌ Teste 5: Validação - user_id inválido

**Endpoint:** `POST http://localhost:5000/recomendar`

**Body (JSON):**
```json
{
  "user_id": 9999,
  "n_recomendacoes": 5
}
```

**Resposta esperada:**
```json
{
  "erro": "user_id deve estar entre 1 e 943"
}
```
**Status Code:** 400

---

## ❌ Teste 6: Validação - Content-Type incorreto

**Endpoint:** `POST http://localhost:5000/recomendar`

**Headers:**
```
Content-Type: text/plain
```

**Resposta esperada:**
```json
{
  "erro": "Content-Type deve ser application/json"
}
```
**Status Code:** 400

---

## 🎯 Exemplos de Uso

### Exemplo 1: 10 recomendações para usuário 50
```json
{
  "user_id": 50,
  "n_recomendacoes": 10
}
```

### Exemplo 2: 3 recomendações para usuário 200
```json
{
  "user_id": 200,
  "n_recomendacoes": 3
}
```

### Exemplo 3: Padrão (5 recomendações)
```json
{
  "user_id": 100
}
```

---

## 📝 Notas

- `user_id` válido: 1 a 943
- `n_recomendacoes` válido: 1 a 50
- `n_recomendacoes` é opcional (padrão: 5)
- Sempre use `Content-Type: application/json`
