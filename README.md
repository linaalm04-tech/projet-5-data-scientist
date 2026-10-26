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

## Documentation technique du modèle de Machine Learning

### Fonctionnement du modèle

Le modèle de Machine Learning est utilisé pour réaliser des prédictions à partir des données des employés. Il est enregistré dans le fichier `model.joblib` puis chargé par l’API FastAPI afin de produire des prédictions à partir des données reçues.

Le modèle doit recevoir les variables attendues dans le même format que celui utilisé lors de son entraînement. Les données doivent être préparées de manière cohérente afin d’éviter les erreurs lors de la prédiction.

### Évaluation des performances

Les performances du modèle doivent être évaluées sur un jeu de données de test distinct de celui utilisé pour l’entraînement. Cette étape permet de vérifier sa capacité à produire des prédictions sur de nouvelles données.

Les indicateurs d’évaluation doivent être choisis en fonction du problème traité. Pour une classification, on peut notamment utiliser :
- **Accuracy** : proportion de prédictions correctes.
- **Précision** : proportion de prédictions positives qui sont correctes.
- **Recall (rappel)** : proportion de cas positifs correctement identifiés.
- **F1-score** : équilibre entre la précision et le rappel.

Les valeurs obtenues lors de l’évaluation doivent être ajoutées à cette documentation à partir des résultats réels du modèle. Elles permettent de suivre son évolution au fil des mises à jour.

### Choix techniques

- **Scikit-learn** : entraînement et utilisation du modèle de Machine Learning.
- **Joblib** : sauvegarde et chargement du modèle dans `model.joblib`.
- **FastAPI** : mise à disposition du modèle via une API.
- **Pytest** : vérification du bon fonctionnement de l’API et de ses fonctionnalités.

Ces outils permettent de séparer le modèle, l’API et les tests, et facilitent la maintenance du projet.

## Maintenance et mise à jour du modèle

### Vérification des performances

Le modèle doit être évalué régulièrement à partir de nouvelles données représentatives. Les prédictions obtenues doivent être comparées aux résultats réels lorsque ceux-ci sont disponibles. Les métriques d’évaluation doivent ensuite être comparées à celles du modèle actuel afin de détecter une éventuelle baisse de performance.

### Réentraînement du modèle

Si les performances diminuent ou si les données évoluent, le modèle peut être réentraîné avec des données récentes et correctement préparées. Les mêmes étapes de préparation des données et la même méthode d’évaluation doivent être conservées afin de comparer les résultats de manière cohérente.

### Tests du nouveau modèle

Avant son déploiement, le nouveau modèle doit être évalué sur un jeu de test indépendant. Il faut vérifier ses performances, s’assurer qu’il accepte les données attendues et exécuter les tests de l’API avec :

```bash
python -m pytest
```

Le nouveau modèle ne doit être retenu que si les tests passent et si ses performances sont satisfaisantes.

### Remplacement du modèle

1. Conserver une copie de sauvegarde de l’ancien fichier `model.joblib`.
2. Enregistrer le nouveau modèle au format Joblib sous le nom `model.joblib`.
3. Remplacer l’ancien fichier par le nouveau dans le projet.
4. Redémarrer l’API afin qu’elle charge le nouveau modèle.
5. Vérifier le fonctionnement de l’API et exécuter les tests.
6. En cas de problème, restaurer la sauvegarde de l’ancien modèle.

### Suivi et maintenance régulière

Il est recommandé de conserver un historique des versions du modèle, des dates de réentraînement, des métriques obtenues et des modifications effectuées. Cette démarche facilite le suivi des performances et permet de revenir à une version précédente en cas de régression.
