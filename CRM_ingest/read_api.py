import polars as pl
import requests

# Lê os dados da API
url = "https://LuisVieira.pythonanywhere.com/api/oportunidades"
res = requests.get(url).json()

# Cria o DataFrame base
df = pl.from_dicts(res)

# Explode contatos (pega o primeiro da lista)
df = df.with_columns([
    pl.col("contacts").list.get(0).struct.rename_fields(["contact_id", "contact_name"]).alias("contact")
])
df = df.unnest("contact")

# Renomeia e expande os campos aninhados
df = df.with_columns([
    pl.col("organization").struct.rename_fields(["organization_id", "organization_name"]),
    pl.col("deal_stage").struct.rename_fields(["deal_stage_id", "deal_stage_name"]),
    pl.col("deal_pipeline").struct.rename_fields(["deal_pipeline_id", "deal_pipeline_name"]),
]).unnest(["organization", "deal_stage", "deal_pipeline"])

# Extrai os campos customizados
def extract_custom(field_id: str):
    return pl.col("custom_fields").list.eval(
        pl.when(pl.element().struct.field("custom_field_id") == field_id)
        .then(pl.element().struct.field("value"))
        .otherwise(None)
    ).list.drop_nulls().list.get(0)

df = df.with_columns([
    extract_custom("cf_produto_interesse").alias("produto_interesse"),
    extract_custom("cf_canal_aquisicao").alias("canal_aquisicao")
])

# Remove a coluna original de custom_fields
df = df.drop("custom_fields")

# Converte para pandas e salva como XLSX
df.to_pandas().to_excel("oportunidades_RD_simulada.xlsx", index=False)

print("Arquivo .xlsx gerado com sucesso!")
