# projet-5-data-scientist
Mise en place d'un environnement de développement et CI/CD
## Installation 
###  1. cloner le projet 
```bash
git clone <URL_DU_REPOSITORY>
cd projet-5-data-scientist
Créer l'environnement virtuel
Bash
python3 -m venv .venv
source .venv/bin/activate
Installer les dépendances 
Bash
python -m pip install -r requirements.txt
Lancer les tests
pytest

## Lancement de l'API

Depuis la racine du projet, activer l'environnement virtuel puis lancer :

```bash
uvicorn src.api:app --reload

L'API est accessible à l'adresse `http://127.0.0.1:8000`.

La documentation interactive Swagger est disponible sur `http://127.0.0.1:8000/docs`.

## Base de données PostgreSQL

Le projet utilise PostgreSQL pour stocker les données des demandes de prédiction et les résultats produits par le modèle.

Les tables utilisées sont :

- `employees` : contient le dataset RH.
- `prediction_requests` : conserve les données envoyées à l'API.
- `prediction_results` : conserve les prédictions associées aux demandes.

SQLAlchemy est utilisé pour gérer les interactions entre Python et la base de données.

Le schéma et les relations entre les tables sont documentés dans `schema_bdd.md`.

Pour vérifier ou créer les tables définies dans les modèles SQLAlchemy :

```bash
python -m src.create_db

## Tests

Pour lancer les tests de l'API :

```bash
python -m pytest -v src/tests/test_api.py
```

Pour consulter la couverture des tests :

```bash
python -m pytest --cov=src --cov-report=term-missing
## Documentation de l’API

La documentation interactive est accessible via :
http://127.0.0.1:8000/docs
## Modèle de Machine Learning

Le modèle permet de réaliser des prédictions à partir des données des employés.
Il est chargé par l’API depuis le fichier `model.joblib`.

## Base de données

La base de données conserve les demandes envoyées à l’API et les résultats des prédictions.
Le schéma est détaillé dans `schema_bdd.md`.

## Maintenance

Le modèle doit être réévalué régulièrement à l’aide de nouvelles données afin de vérifier ses performances.

## Architecture du projet

- `src/api.py` : gestion de l’API FastAPI et des prédictions.
- `src/models.py` : définition des modèles de données.
- `src/database.py` : connexion à la base de données.
- `src/create_db.py` : création des tables.
- `src/tests/` : tests de l’API.
- `model.joblib` : modèle de Machine Learning sauvegardé.
- `schema_bdd.md` : documentation du schéma de la base de données.

## Exemple d’utilisation

Lancer l’API :

```bash
uvicorn src.api:app --reload
Ouvrir ensuite la documentation interactive :
http://127.0.0.1:8000/docs

## Mise à jour du modèle

Avant de remplacer le modèle, vérifier ses performances sur de nouvelles données.
Le nouveau modèle doit être testé avant d’être déployé en production.