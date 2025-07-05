"""
Utilitários comuns para os geradores de dados sintéticos
Autor: Luis Guilherme · Vieira Company
"""

import random, csv, json, datetime as dt
from pathlib import Path
from typing import List, Dict


# ------------------------------------------------------------------
# Funções auxiliares
# ------------------------------------------------------------------

def rand_date(start: dt.date, end: dt.date) -> dt.date:
    """Data aleatória (datetime.date) entre start e end, inclusivo."""
    delta = (end - start).days
    return start + dt.timedelta(days=random.randint(0, delta))


def make_seq_id(prefix: str, n: int) -> str:
    """ID sequencial no formato PREFIX-000001."""
    return f"{prefix}-{n:06d}"


def write_json_csv(name: str, rows: List[Dict], base_dir: Path) -> None:
    """
    Salva `rows` em JSON e CSV dentro de `base_dir`.
    - Se a pasta não existir, será criada.
    - O schema (colunas) é derivado das chaves do 1º dicionário.
    """
    base_dir.mkdir(parents=True, exist_ok=True)

    json_path = base_dir / f"{name}.json"
    csv_path  = base_dir / f"{name}.csv"

    # JSON
    with json_path.open("w", encoding="utf-8") as jf:
        json.dump(rows, jf, ensure_ascii=False, indent=2)

    # CSV
    with csv_path.open("w", newline="", encoding="utf-8") as cf:
        writer = csv.DictWriter(cf, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"{name}: {len(rows):,} registros salvos → {json_path}")
