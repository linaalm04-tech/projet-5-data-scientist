from pathlib import Path

import pandas as pd
from sqlalchemy import text

from src.database import engine


def import_employees():
    # Chemin vers le fichier CSV à la racine du projet
    csv_path = Path(__file__).resolve().parent.parent / "employees_export.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {csv_path}")

    # Lecture des données
    df = pd.read_csv(csv_path)

    if df.empty:
        raise ValueError("Le fichier CSV ne contient aucune donnée.")

    # Vérification pour éviter les doublons
    with engine.begin() as connection:
        count = connection.execute(
            text("SELECT COUNT(*) FROM employees")
        ).scalar_one()

        if count > 0:
            print(
                f"Import annulé : la table contient déjà {count} employés."
            )
            return

        # Import uniquement si la table est vide
        df.to_sql(
            "employees",
            con=connection,
            if_exists="append",
            index=False,
        )

    print(f"{len(df)} employés importés avec succès.")


if __name__ == "__main__":
    import_employees()