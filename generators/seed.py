"""
Gerador de organizações e contatos (entidades mestre)
"""

import uuid, random
from pathlib import Path
from typing import Tuple, List, Dict
from .utils import write_csv_and_upload_s3

__all__ = ["run"]

def _generate_orgs(n: int) -> List[Dict]:
    return [{
        "org_id": str(uuid.uuid4()),
        "name": f"Empresa {i}"
    } for i in range(1, n + 1)]

def _generate_contacts(orgs: List[Dict]) -> List[Dict]:
    contacts = []
    for org in orgs:
        contacts.append({
            "contact_id": str(uuid.uuid4()),
            "org_id": org["org_id"],
            "name": f"Contato {org['name']}",
            "email": f"contato{random.randint(1,9999)}@{org['name'].lower().replace(' ', '')}.com"
        })
    return contacts

def run(base_dir: Path, n_org: int = 1000, bucket: str = "rocha-lake", s3_folder: str = "bronze", region: str = "us-east-1", aws_access_key_id: str = None, aws_secret_access_key: str = None) -> Tuple[List[Dict], List[Dict]]:
    """
    Gera n organizações e seus respectivos contatos.
    Salva em CSV local e envia para S3: organizations_rd e contacts_rd
    """
    orgs = _generate_orgs(n_org)
    contacts = _generate_contacts(orgs)

    write_csv_and_upload_s3("organizations_rd", orgs, base_dir, bucket, s3_folder, region, aws_access_key_id, aws_secret_access_key)
    write_csv_and_upload_s3("contacts_rd", contacts, base_dir, bucket, s3_folder, region, aws_access_key_id, aws_secret_access_key)

    return orgs, contacts
