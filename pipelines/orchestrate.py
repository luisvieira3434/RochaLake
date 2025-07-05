from pathlib import Path
import datetime as dt
from ..generators import seed, rd, erp

__all__ = ["main"]


def main(out_dir: str | Path = "data") -> None:
    # Raiz do projeto baseada neste arquivo: .../vieira_company
    project_root = Path(__file__).parent.parent.resolve()

    # Pasta do timestamp dentro de <project_root>/data/
    ts_folder = project_root / out_dir / dt.date.today().isoformat()
    ts_folder.mkdir(parents=True, exist_ok=True)

    # 1. Organizações & Contatos
    orgs, contacts = seed.run(ts_folder, n_org=1000)

    # 2. CRM – RD Station
    deals = rd.run(ts_folder, orgs, dt.date(2025, 1, 1), dt.date(2025, 6, 30))

    # 3. ERP – Oracle NetSuite (somente oportunidades ganhas)
    deals_won = [d for d in deals if d["status"] == "won"]
    erp.generate_erp(deals_won, ts_folder)

    print(f"🎉  Dados sintéticos gerados em {ts_folder}")
    print(f"     → {ts_folder.relative_to(project_root)}")


if __name__ == "__main__":
    main()
