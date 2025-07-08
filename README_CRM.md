# 🤖 CRM Ingest – Simulação de API Estilo RD Station

Este módulo simula dados de oportunidades comerciais no formato da API da **RD Station**.  
É ideal para testes de ingestão, construção de pipelines de dados, prototipação de dashboards e integração com ferramentas como Power BI, Databricks ou Streamlit.

---

## 📁 Estrutura do Módulo

| Arquivo | Descrição |
|---------|-----------|
| `crm_data_generator.py` | Gera 100.000 registros de oportunidades e salva no arquivo `data.json` |
| `api_main.py` | Sobe uma API local usando Flask, servindo os dados gerados |
| `read_api.py` | Consome a API, processa os dados com Polars e exporta para Excel (.xlsx) |

---

## 📦 Bibliotecas Utilizadas

### 🧩 Bibliotecas padrão do Python
- `json` – manipulação e serialização dos dados
- `os` – leitura de arquivos e caminhos
- `random` – geração de dados simulados
- `datetime` – controle de datas e horários

### 🚀 Bibliotecas externas
- `flask` – criação da API local
- `requests` – consumo da API HTTP
- `polars` – manipulação de dados com alta performance
- `pandas` – exportação para Excel e compatibilidade com Power BI
- `openpyxl` – engine para exportação `.xlsx`

### ✅ Instalação:
```bash
pip install flask requests polars pandas openpyxl