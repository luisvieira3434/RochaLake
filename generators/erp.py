"""
Gerador de dados simulados do ERP Oracle NetSuite:
→ Faturas (invoices), pagamentos (payments), razão geral (GL)
"""

import datetime as dt
import random
from pathlib import Path
from typing import List, Dict
from .utils import make_seq_id, write_csv_and_upload_s3

__all__ = ["generate_erp"]

def generate_erp(
    deals_won: List[Dict],
    base_dir: Path,
    bucket: str = "rocha-lake",
    s3_folder: str = "bronze",
    region: str = "us-east-1",
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None
):
    invoices, payments, gls = [], [], []
    inv_seq = pay_seq = gl_seq = 1

    for d in deals_won:
        issue = dt.date.fromisoformat(d["closing_date"]) if d.get("closing_date") else dt.date.fromisoformat(d["created_at"][:10])
        issue += dt.timedelta(days=random.randint(0, 5))
        inv_id = make_seq_id("INV", inv_seq)
        inv_seq += 1

        # Fatura
        invoices.append({
            "invoice_id": inv_id,
            "deal_id": d["id"],
            "org_id": d["organization"]["id"],
            "amount": d["value"],
            "issue_date": issue.isoformat(),
            "currency": "BRL",
            "status": "Open",
            "source_system": "Oracle NetSuite"
        })

        # Pagamento
        pay_date = issue + dt.timedelta(days=random.randint(5, 30))
        pay_id = make_seq_id("PAY", pay_seq)
        pay_seq += 1

        payments.append({
            "payment_id": pay_id,
            "invoice_id": inv_id,
            "amount": d["value"],
            "payment_date": pay_date.isoformat(),
            "method": random.choice(["PIX", "TED", "Boleto"]),
            "source_system": "Oracle NetSuite"
        })

        # Razão Geral (GL) – débito/crédito
        for side, acc in [("debit", "1.1.2 Banco"), ("credit", "3.1.1 Receita")]:
            gl_id = make_seq_id("GL", gl_seq)
            gl_seq += 1

            gls.append({
                "gl_id": gl_id,
                "invoice_id": inv_id,
                "account": acc,
                "debit": d["value"] if side == "debit" else 0,
                "credit": d["value"] if side == "credit" else 0,
                "post_date": pay_date.isoformat(),
                "source_system": "Oracle NetSuite"
            })

    # Salva tudo
    write_csv_and_upload_s3("invoices_netsuite", invoices, base_dir, bucket, s3_folder, region, aws_access_key_id, aws_secret_access_key)
    write_csv_and_upload_s3("payments_netsuite", payments, base_dir, bucket, s3_folder, region, aws_access_key_id, aws_secret_access_key)
    write_csv_and_upload_s3("gl_netsuite", gls, base_dir, bucket, s3_folder, region, aws_access_key_id, aws_secret_access_key)

    return invoices, payments, gls