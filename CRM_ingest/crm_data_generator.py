import json
import random
import datetime
import os

# Função para gerar uma data aleatória dentro de um intervalo
def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + datetime.timedelta(days=random_days)

# Listas de exemplo (20 itens em cada)
nomes = [
    "Análise de Mercado para Nova Startup",
    "Modelo de Previsão de Vendas",
    "Data Warehouse para Finanças",
    "Inteligência Artificial para Indústria Automotiva",
    "Automação de Processos Empresariais",
    "Plataforma de E-commerce Personalizada",
    "Solução de CRM para Pequenas Empresas",
    "Sistema de Gestão para Restaurantes",
    "Software de Controle Financeiro",
    "Análise de Big Data para Marketing",
    "Otimização de Cadeia de Suprimentos",
    "Desenvolvimento de Aplicativo Móvel",
    "Implementação de Sistemas ERP",
    "Soluções de Segurança da Informação",
    "Análise de Dados para Varejo",
    "Consultoria em Transformação Digital",
    "Integração de Sistemas Legados",
    "Modernização de Infraestrutura de TI",
    "Planejamento Estratégico de TI",
    "Desenvolvimento de Software Sob Medida"
]

segments = [
    "Tecnologia de Informação",
    "Varejo",
    "Serviços Financeiros",
    "Indústria Automotiva",
    "Educação",
    "Saúde",
    "Agronegócio",
    "Energia",
    "Telecomunicações",
    "E-commerce",
    "Turismo",
    "Imobiliário",
    "Logística",
    "Entretenimento",
    "Construção",
    "Moda",
    "Alimentação",
    "Beleza",
    "Serviços Públicos",
    "Consultoria Empresarial"
]

produtos_interesse = [
    "Consultoria de Dados",
    "Análise de Mercado",
    "Consultoria em Dados",
    "Soluções Personalizadas",
    "Implementação de ERP",
    "Serviços de Cloud Computing",
    "Automação de Marketing",
    "Desenvolvimento de Chatbots",
    "Gestão de Projetos Digitais",
    "Treinamento de Equipes de TI",
    "Desenvolvimento Web",
    "Desenvolvimento Mobile",
    "Análise de Redes Sociais",
    "Otimização de SEO",
    "Design de UX/UI",
    "Integração de Sistemas",
    "Suporte Técnico 24/7",
    "Gerenciamento de Dados",
    "Consultoria em Segurança",
    "Desenvolvimento de API"
]

# Lista de canais de aquisição (mantendo 10 itens)
canais_aquisicao = [
    "LinkedIn",
    "Site",
    "Referência",
    "Google",
    "Feira de Negócios",
    "Indicação",
    "Instagram",
    "YouTube",
    "Email Marketing",
    "Webinar"
]

# Outras listas para campos adicionais
project_managers = ["Alice", "Bruno", "Carlos", "Diana", "Eduardo", "Fernanda", "Gabriel", "Helena", "Isabela", "João"]
contract_types = ["Fixed", "Hourly", "Retainer", "Milestone"]
statuses = ["Pending", "In Progress", "Completed", "Canceled"]
priorities = ["Low", "Medium", "High"]
client_categories = ["Small Business", "Enterprise", "Startup", "Government", "Non-profit", "Individual", "Educational", "Corporate", "Freelancer", "Other"]
notes_list = [
    "Nenhuma observação.",
    "Projeto desafiador.",
    "Reunião marcada para próxima semana.",
    "Cliente muito interessado.",
    "Revisão do contrato pendente.",
    "Aguardando aprovação final.",
    "Projeto com alto potencial.",
    "Precisa de mais recursos.",
    "Reunião com stakeholders agendada.",
    "Follow-up necessário."
]

# Datas base para os campos de data/hora
data_pred_start = datetime.date(2025, 3, 30)
data_pred_end = datetime.date(2025, 4, 30)
data_created_base = datetime.datetime(2025, 3, 1, 12, 0, 0)
data_updated_base = datetime.datetime(2025, 3, 15, 15, 30, 0)

# Defina o número de registros que deseja gerar (100.000)
limit = 100000

oportunidades = []

for i in range(1, limit + 1):
    nome_escolhido = random.choice(nomes)
    valor = random.choice([15000.0, 20000.0, 30000.0, 40000.0, 50000.0])
    created_at = data_created_base + datetime.timedelta(days=random.randint(0, 5))
    updated_at = data_updated_base + datetime.timedelta(days=random.randint(0, 5))
    closing_date = random_date(data_pred_start, data_pred_end)

    status = random.choice(["open", "won", "lost"])
    deal_stage = {
        "id": f"stage_{random.randint(1,5)}",
        "name": random.choice([
            "Lead Qualificado", "Proposta Enviada", "Negociação", "Fechamento", "Pós-venda"
        ])
    }
    deal_pipeline = {
        "id": f"pipeline_{random.randint(1, 3)}",
        "name": random.choice([
            "Funil Comercial", "Funil de Pré-vendas", "Funil de Expansão"
        ])
    }
    organization = {
        "id": f"org_{random.randint(1, 100)}",
        "name": f"Empresa {i}"
    }
    contact = {
        "id": f"contact_{i}",
        "name": f"Contato {i}"
    }

    produto = random.choice(produtos_interesse)
    canal = random.choice(canais_aquisicao)

    oportunidade = {
        "id": f"deal_{i}",
        "title": nome_escolhido,
        "value": valor,
        "currency": "BRL",
        "won": True if status == "won" else False,
        "status": status,
        "deal_stage": deal_stage,
        "deal_pipeline": deal_pipeline,
        "created_at": created_at.isoformat() + "Z",
        "updated_at": updated_at.isoformat() + "Z",
        "closing_date": closing_date.isoformat(),
        "organization": organization,
        "contacts": [contact],
        "custom_fields": [
            {
                "custom_field_id": "cf_produto_interesse",
                "label": "Produto de Interesse",
                "value": produto
            },
            {
                "custom_field_id": "cf_canal_aquisicao",
                "label": "Canal de Aquisição",
                "value": canal
            }
        ]
    }

    oportunidades.append(oportunidade)

# Caminho onde o arquivo JSON será salvo
file_path = r"C:\Users\LuisGuilhermeVieiraR\Desktop\vieira_company\data.json"

# Cria o diretório se não existir
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Grava o conteúdo em um arquivo JSON com indentação para melhor visualização
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(oportunidades, f, ensure_ascii=False, indent=2)

print(f"Arquivo JSON gerado com sucesso em: {file_path}")
