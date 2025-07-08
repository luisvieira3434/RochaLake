"""
Gerador de oportunidades simuladas (CRM – RD Station)
"""

import uuid, random, datetime as dt
from pathlib import Path
from typing import List, Dict
from .utils import rand_date, write_csv_and_upload_s3

__all__ = ["run"]

# Listas de campos customizados
TITULOS = [
    "Análise de Mercado para Nova Startup", "Modelo de Previsão de Vendas",
    "Data Warehouse para Finanças", "IA para Indústria Automotiva",
    "Automação de Processos Empresariais", "E-commerce Personalizado",
    "CRM para Pequenas Empresas", "Sistema de Gestão para Restaurantes",
    "Software de Controle Financeiro", "Big Data para Marketing",
    "Otimização de Suprimentos", "Aplicativo Móvel B2B",
    "Sistemas ERP Cloud", "Segurança da Informação",
    "Dados para Varejo", "Transformação Digital",
    "Integração de Sistemas Legados", "Infraestrutura de TI Moderna",
    "Planejamento Estratégico Digital", "Software Sob Medida"
]

PRODUTOS = [
    "Consultoria de Dados", "Análise de Mercado", "Soluções Personalizadas",
    "Implementação de ERP", "Cloud Computing", "Automação de Marketing",
    "Chatbots", "Projetos Digitais", "Treinamento de TI",
    "Desenvolvimento Web", "Mobile Apps", "Análise de Redes Sociais",
    "SEO", "UX/UI Design", "Integração de Sistemas", "Suporte Técnico",
    "Gestão de Dados", "Segurança de Informação", "APIs", "ETL/ELT"
]

CANAIS = [
    "LinkedIn", "Site", "Referência", "Google", "Feira de Negócios",
    "Indicação", "Instagram", "YouTube", "Email Marketing", "Webinar"
]

def _generate_deal(org: Dict, seq: int, start: dt.date, end: dt.date) -> Dict:
    created = rand_date(start, end)
    updated = created + dt.timedelta(days=random.randint(1, 5))
    closing = created + dt.timedelta(days=random.randint(5, 30))

    value = random.choice([15000, 20000, 30000, 40000, 50000])
    status = random.choice(["open", "won", "lost"])
    won_flag = status == "won"

    return {
        "id": f"deal_{seq}",
        "title": random.choice(TITULOS),
        "value": value,
        "currency": "BRL",
        "won": won_flag,
        "status": status,
        "deal_stage": {
            "id": f"stage_{random.randint(1,5)}",
            "name": random.choice(["Lead Qualificado", "Proposta Enviada", "Negociação", "Fechamento", "Pós-venda"])
        },
        "deal_pipeline": {
            "id": f"pipeline_{random.randint(1,3)}",
            "name": random.choice(["Funil Comercial", "Pré-vendas", "Expansão"])
        },
        "created_at": created.isoformat() + "Z",
        "updated_at": updated.isoformat() + "Z",
        "closing_date": closing.isoformat() if won_flag else None,
        "organization": {"id": org["org_id"], "name": org["name"]},
        "contacts": [{"id": f"contact_{seq}", "name": f"Contato {seq}"}],
        "custom_fields": [
            {"custom_field_id": "cf_produto_interesse", "label": "Produto de Interesse", "value": random.choice(PRODUTOS)},
            {"custom_field_id": "cf_canal_aquisicao", "label": "Canal de Aquisição", "value": random.choice(CANAIS)}
        ],
        "source_system": "RD Station"
    }

def run(
    base_dir: Path,
    orgs: List[Dict],
    start: dt.date,
    end: dt.date,
    max_deals: int = 5,
    bucket: str = "rocha-lake",
    s3_folder: str = "bronze",
    region: str = "us-east-1",
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None
) -> List[Dict]:
    """Gera oportunidades (deals_rd) para as organizações."""
    deals = []
    seq = 1
    for org in orgs:
        for _ in range(random.randint(1, max_deals)):
            deals.append(_generate_deal(org, seq, start, end))
            seq += 1

    write_csv_and_upload_s3(
        "deals_rd", deals, base_dir, bucket, s3_folder, region, aws_access_key_id, aws_secret_access_key
    )
    return deals