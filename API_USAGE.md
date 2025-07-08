# 🚀 Rochalake Data API - Guia de Uso

API Flask para gerar e baixar dados sintéticos do projeto Rochalake.

## 📋 Endpoints Disponíveis

### ✅ Verificação de Saúde
```bash
GET /api/health
```
Verifica se a API está funcionando.

### 📊 Geração de Dados

#### Gerar Todos os Dados
```bash
POST /api/generate-all
```
Gera todos os tipos de dados (organizações, deals, ERP) de uma vez.

#### Gerar Apenas Organizações
```bash
POST /api/generate-organizations
```
Gera apenas organizações e contatos.

Payload opcional:
```json
{
  "n_organizations": 500
}
```

#### Gerar Deals/Oportunidades
```bash
POST /api/generate-deals
```
Gera oportunidades do CRM (RD Station).

#### Gerar Dados ERP
```bash
POST /api/generate-erp
```
Gera dados do ERP (faturas, pagamentos, GL).

### 📁 Listagem e Download

#### Listar Arquivos Disponíveis
```bash
GET /api/files
```
Lista todos os arquivos CSV gerados com informações de data, tamanho e links de download.

#### Baixar Arquivo Específico
```bash
GET /api/download/<date>/<filename>
```
Exemplo: `GET /api/download/2025-01-08/organizations_rd.csv`

#### Baixar Versão Mais Recente
```bash
GET /api/download/latest/<filename>
```
Exemplo: `GET /api/download/latest/deals_rd.csv`

### ℹ️ Informações da API
```bash
GET /api/info
```
Retorna informações completas sobre todos os endpoints e tipos de dados.

## 🎯 Exemplos de Uso

### Usando curl

1. **Verificar se a API está funcionando:**
```bash
curl http://localhost:5000/api/health
```

2. **Gerar todos os dados:**
```bash
curl -X POST http://localhost:5000/api/generate-all
```

3. **Listar arquivos disponíveis:**
```bash
curl http://localhost:5000/api/files
```

4. **Baixar arquivo específico:**
```bash
curl -O http://localhost:5000/api/download/latest/organizations_rd.csv
```

### Usando Python requests

```python
import requests

# Base URL da API
BASE_URL = "http://localhost:5000/api"

# Gerar todos os dados
response = requests.post(f"{BASE_URL}/generate-all")
print(response.json())

# Listar arquivos
response = requests.get(f"{BASE_URL}/files")
files = response.json()["files"]

# Baixar arquivo
for file_info in files:
    if file_info["filename"] == "deals_rd.csv":
        download_url = f"http://localhost:5000{file_info['download_url']}"
        file_data = requests.get(download_url)
        with open(file_info["filename"], "wb") as f:
            f.write(file_data.content)
```

## 📋 Tipos de Dados Gerados

| Arquivo | Descrição |
|---------|-----------|
| `organizations_rd.csv` | Organizações base (empresas) |
| `contacts_rd.csv` | Contatos das organizações |
| `deals_rd.csv` | Oportunidades/deals do CRM |
| `invoices_netsuite.csv` | Faturas do ERP |
| `payments_netsuite.csv` | Pagamentos do ERP |
| `gl_netsuite.csv` | Lançamentos contábeis |

## 🔧 Como Executar

1. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

2. **Executar a API:**
```bash
python app.py
```

3. **Acessar no navegador:**
```
http://localhost:5000/api/info
```

A API estará disponível em `http://localhost:5000`

## 📁 Estrutura de Arquivos

Os arquivos são organizados por data na pasta `data/`:
```
data/
├── 2025-01-08/
│   ├── organizations_rd.csv
│   ├── contacts_rd.csv
│   ├── deals_rd.csv
│   ├── invoices_netsuite.csv
│   ├── payments_netsuite.csv
│   └── gl_netsuite.csv
└── 2025-01-09/
    └── ...
```