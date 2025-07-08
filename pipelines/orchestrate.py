from pathlib import Path
import datetime as dt
from dotenv import load_dotenv
import os
from ..generators import seed, rd, erp

__all__ = ["main"]

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET = os.getenv("BUCKET", "rocha-lake")
S3_FOLDER = os.getenv("S3_FOLDER", "bronze")
REGION = os.getenv("REGION", "us-east-1")

def main(out_dir: str | Path = "data") -> None:
    # Raiz do projeto baseada neste arquivo: .../vieira_company
    project_root = Path(__file__).parent.parent.resolve()

    # Pasta do timestamp dentro de <project_root>/data/
    ts_folder = project_root / out_dir / dt.date.today().isoformat()
    ts_folder.mkdir(parents=True, exist_ok=True)

    # Organizações & Contatos
    orgs, contacts = seed.run(
        ts_folder, n_org=1000,
        bucket=BUCKET, s3_folder=S3_FOLDER, region=REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    # CRM – RD Station
    deals = rd.run(
        ts_folder, orgs, dt.date(2025, 1, 1), dt.date(2025, 6, 30),
        bucket=BUCKET, s3_folder=S3_FOLDER, region=REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    # ERP – Oracle NetSuite (somente oportunidades ganhas)
    deals_won = [d for d in deals if d["status"] == "won"]
    erp.generate_erp(
        deals_won, ts_folder,
        bucket=BUCKET, s3_folder=S3_FOLDER, region=REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    print(f"🎉  Dados sintéticos gerados em {ts_folder}")
    print(f"     → {ts_folder.relative_to(project_root)}")


if __name__ == "__main__":
    main()