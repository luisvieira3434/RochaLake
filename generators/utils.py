"""
Utilitários comuns para os geradores de dados sintéticos
Autor: Luis Guilherme · Vieira Company
"""

import random, csv, datetime as dt
from pathlib import Path
from typing import List, Dict, Optional
import boto3
from botocore.exceptions import NoCredentialsError

def rand_date(start: dt.date, end: dt.date) -> dt.date:
    """Data aleatória (datetime.date) entre start e end, inclusivo."""
    delta = (end - start).days
    return start + dt.timedelta(days=random.randint(0, delta))


def make_seq_id(prefix: str, n: int) -> str:
    """ID sequencial no formato PREFIX-000001."""
    return f"{prefix}-{n:06d}"


def write_csv_and_upload_s3(
    name: str,
    rows: List[Dict],
    base_dir: Path,
    bucket: str,
    s3_folder: str = "",
    region: str = "us-east-1",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None
) -> None:
    """
    Salva `rows` em CSV dentro de `base_dir` e faz upload para o S3.
    - Se a pasta não existir, será criada.
    - O schema (colunas) é derivado das chaves do 1º dicionário.
    """
    base_dir.mkdir(parents=True, exist_ok=True)
    csv_path = base_dir / f"{name}.csv"

    # CSV
    with csv_path.open("w", newline="", encoding="utf-8") as cf:
        writer = csv.DictWriter(cf, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"{name}: {len(rows):,} registros salvos → {csv_path}")

    # Upload para S3
    s3_key = f"{s3_folder}/{name}.csv" if s3_folder else f"{name}.csv"
    s3_key = s3_key.lstrip("/")
    try:
        s3 = boto3.client(
            "s3",
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        s3.upload_file(str(csv_path), bucket, s3_key)
        print(f"Arquivo enviado para S3: s3://{bucket}/{s3_key}")
    except NoCredentialsError:
        print("Credenciais AWS não encontradas. Configure via variáveis de ambiente ou arquivo ~/.aws/credentials.")
    except Exception as e:
        print(f"Erro ao enviar para S3: {e}")
