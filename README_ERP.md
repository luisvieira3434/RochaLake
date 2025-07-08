# ERP Ingest – Simulação de Dados Oracle NetSuite

Este módulo simula dados financeiros no formato de sistemas ERP como o **Oracle NetSuite**.  
É ideal para testes de ingestão, construção de pipelines de dados financeiros, prototipação de relatórios e integração com ferramentas como Power BI, Databricks ou Streamlit.

---

## Estrutura do Módulo

| Arquivo | Descrição |
|---------|-----------|
| `erp.py` | Gera registros simulados de faturas (invoices), pagamentos (payments) e razão geral (GL) |

---

## Bibliotecas Utilizadas

### Bibliotecas padrão do Python
- `random` – geração de dados simulados
- `datetime` – controle de datas e horários
- `pathlib` – manipulação de caminhos

### Bibliotecas externas
- `boto3` – integração com Amazon S3 para upload dos arquivos CSV

### Instalação:
```bash
pip install boto3
```

---

## Como executar

1. Configure suas credenciais AWS em um arquivo `.env` ou diretamente no script.
2. Execute o pipeline de geração de dados:

```bash
python executa_seed.py
```

Os arquivos CSV serão gerados localmente e enviados automaticamente para o bucket S3 configurado.

---

## Saídas Geradas

- `invoices_netsuite.csv` – Faturas simuladas
- `payments_netsuite.csv` – Pagamentos simulados
- `gl_netsuite.csv` – Lançamentos de razão geral simulados

---

## Observações
- Os dados são totalmente sintéticos e podem ser customizados conforme a necessidade.
- O upload para S3 depende de credenciais válidas e permissões adequadas.
