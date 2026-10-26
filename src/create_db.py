
from src.database import Base, engine
from src import models


def create_tables():
    """Créer les tables définies dans les modèles SQLAlchemy."""
    Base.metadata.create_all(bind=engine)
    print("Les tables de la base de données sont prêtes.")


if __name__ == "__main__":
    create_tables()

