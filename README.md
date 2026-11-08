Projet 5 – Data Scientist

Mise en place d'un environnement de développement, d'une API de Machine Learning et d'un processus d'intégration continue (CI).

Dépôt GitHub : https://github.com/linaalm04-tech/projet-5-data-scientist

1. Présentation du projet

Ce projet consiste à mettre en place un environnement permettant d'exposer un modèle de Machine Learning à travers une API développée avec FastAPI.

L'application permet de recevoir des données relatives aux employés, de produire une prédiction à l'aide du modèle entraîné et de conserver les demandes ainsi que les résultats dans une base de données PostgreSQL.

Le projet intègre également des tests automatisés avec Pytest et un workflow GitHub Actions afin de vérifier le bon fonctionnement du code lors des modifications.

2. Prérequis

Les outils nécessaires au fonctionnement du projet sont :

Python 3.9.4 ;

PostgreSQL ;

Git ;

pip ;

un environnement virtuel Python ;

les dépendances indiquées dans requirements.txt.

Le projet a été développé et testé localement sur macOS avec Python 3.9.4, dans un environnement virtuel.

Le workflow GitHub Actions utilise Python 3.11 et Ubuntu pour exécuter les tests automatisés.

3. Installation et configuration

3.1. Cloner le dépôt

git clone https://github.com/linaalm04-tech/projet-5-data-scientist.git
cd projet-5-data-scientist

3.2. Créer un environnement virtuel

python3 -m venv .venv

Activer l'environnement virtuel sur macOS ou Linux :

source .venv/bin/activate

3.3. Installer les dépendances

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

3.4. Configuration de PostgreSQL

Le projet utilise PostgreSQL pour stocker les données des employés, les demandes de prédiction et les résultats associés.

Créer une base de données PostgreSQL nommée projet5 :

CREATE DATABASE projet5;

La connexion à la base est configurée à l'aide de la variable d'environnement DATABASE_URL.

Le fichier src/database.py récupère cette variable. Si elle n'est pas définie, une adresse locale par défaut est utilisée :

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://localhost/projet5"
)

Pour définir la connexion dans le terminal :

export DATABASE_URL="postgresql+psycopg://localhost/projet5"

La valeur doit être adaptée à la configuration réelle de PostgreSQL et aux identifiants de connexion utilisés.

Pour une base de test distincte :

export DATABASE_URL="postgresql+psycopg://localhost/projet5_test"

Les informations de connexion contenant des identifiants ne doivent pas être publiées dans le dépôt Git.

3.5. Création des tables

Depuis la racine du projet, exécuter :

python -m src.create_db

Ce script initialise les tables définies dans les modèles SQLAlchemy.

Le schéma et les relations entre les tables sont détaillés dans schema_bdd.md.

4. Gestion des versions, environnements et CI/CD

4.1. Gestion des versions avec Git

Git est utilisé pour suivre les modifications du code source, conserver l'historique du projet et organiser les différentes étapes de développement.

Les principales branches utilisées sont :

main : branche principale du projet.

develop : branche d'intégration des développements.

tests-projet-5 : branche utilisée pour les travaux et corrections du projet.

feature/tests : branche dédiée aux tests automatisés.

feature/ci-test : branche dédiée à la configuration de l'intégration continue.

Les modifications sont enregistrées à l'aide de commits. Les fusions permettent d'intégrer les travaux réalisés sur les branches de développement.

Pour consulter les branches :

git branch -a

Pour consulter l'historique des commits et les fusions :

git log --oneline --graph --decorate --all

4.2. Versionnement par tag

Une version du projet a été identifiée à l'aide d'un tag Git annoté :

v1.0.0

Ce tag permet de retrouver un point de référence dans l'historique du projet. Il a été créé localement puis publié sur le dépôt GitHub.

Pour consulter les tags :

git tag --list

Pour consulter les informations du tag :

git show v1.0.0

Pour publier un nouveau tag :

git push origin nom_du_tag

4.3. Gestion des environnements

Le projet distingue les environnements suivants :

Environnement de développement

L'application est développée et exécutée localement sur macOS dans un environnement virtuel Python. La connexion PostgreSQL est configurée à l'aide de DATABASE_URL.

Environnement de test

Les tests automatisés sont exécutés avec Pytest. Une base PostgreSQL dédiée, nommée projet5_test, permet de séparer les données utilisées pour les tests de celles de la base principale.

GitHub Actions utilise également un service PostgreSQL temporaire afin d'exécuter les tests dans un environnement isolé.

Base principale du projet

La base PostgreSQL projet5 contient les données principales du projet, notamment les employés et les enregistrements des demandes de prédiction.

Le workflow actuel ne réalise pas de déploiement automatique sur un serveur de production. La base principale ne doit donc pas être présentée comme un environnement de production déployé.

4.4. Intégration continue avec GitHub Actions

Le projet utilise GitHub Actions pour automatiser les vérifications à chaque événement push ou pull_request.

Le workflow est défini dans :

.github/workflows/ci.yml

Les principales étapes sont :

Récupération du code source avec actions/checkout@v4.

Installation de Python 3.11 avec actions/setup-python@v5.

Mise à jour de pip et installation des dépendances.

Démarrage d'un service PostgreSQL 15.

Vérification de la disponibilité de PostgreSQL grâce à la commande pg_isready.

Création des tables de la base de données.

Exécution des tests automatisés avec Pytest.

Le workflow utilise une base PostgreSQL temporaire nommée project5, dédiée à l'exécution des tests.

Les exécutions du workflow ont été vérifiées sur GitHub Actions et une exécution réussie a été constatée.

4.5. Gestion des identifiants et des variables d'environnement

La connexion PostgreSQL est paramétrée dans src/database.py à l'aide de la variable d'environnement DATABASE_URL.

Cette configuration permet d'utiliser différentes bases de données sans modifier directement le code source.

Dans le workflow GitHub Actions, les identifiants PostgreSQL sont définis pour le service temporaire de test. Ils ne correspondent pas aux identifiants de la base principale.

Les identifiants de test sont actuellement déclarés directement dans le fichier CI. Ils sont réservés à cet environnement temporaire et ne doivent pas être réutilisés pour une base réelle.

Aucun secret de dépôt GitHub n'est actuellement configuré. Pour un futur déploiement, les identifiants sensibles devront être stockés dans les secrets GitHub ou dans un gestionnaire de secrets adapté.

Les fichiers contenant des informations sensibles, notamment .env, sont exclus du suivi Git grâce au fichier .gitignore.

4.6. Déploiement et mise à jour

Le projet dispose actuellement d'un processus d'exécution local de l'API FastAPI.

Pour démarrer l'application :

./.venv/bin/python -m uvicorn src.api:app --reload

Le workflow GitHub Actions assure l'intégration continue, mais aucun déploiement automatique en production n'est configuré.

Pour mettre à jour le projet localement :

Récupérer les modifications depuis le dépôt Git.

Installer les éventuelles nouvelles dépendances.

Vérifier la configuration de la variable DATABASE_URL.

Exécuter les tests automatisés.

Redémarrer l'application.

Vérifier le fonctionnement de l'API et de la base de données.

Pour récupérer les modifications de la branche distante :

git pull

4.7. Retour à une version précédente (rollback)

En cas de problème après une modification, Git permet de retrouver une version antérieure du code.

Le tag v1.0.0 constitue un point de référence pour retrouver la version identifiée du projet.

Pour consulter cette version :

git show v1.0.0

Pour revenir temporairement au code associé à ce tag :

git switch --detach v1.0.0

Pour revenir ensuite à la branche de travail :

git switch tests-projet-5

Cette opération concerne uniquement le code source. La restauration de la base PostgreSQL nécessite une procédure distincte de sauvegarde et de restauration.

4.8. Différence entre intégration continue et déploiement continu

Intégration continue (CI)

L'intégration continue consiste à automatiser les vérifications du code à chaque modification. Dans ce projet, GitHub Actions récupère le code, installe les dépendances, initialise PostgreSQL et exécute les tests Pytest.

Déploiement continu (CD)

Le déploiement continu consiste à automatiser la livraison ou la mise en production d'une application après les vérifications nécessaires.

Dans ce projet, l'intégration continue est mise en place avec GitHub Actions. En revanche, le déploiement automatique en production n'est pas configuré.

5. Lancement et utilisation de l'API

5.1. Démarrer l'API

Depuis la racine du projet, activer l'environnement virtuel puis configurer la clé API :

export API_KEY="$(openssl rand -hex 32)"

Cette commande génère une clé aléatoire pour l'environnement local. La clé doit rester confidentielle et ne doit pas être publiée dans le dépôt Git.

Démarrer ensuite l'application :

./.venv/bin/python -m uvicorn src.api:app --reload

L'API est accessible à l'adresse :

http://127.0.0.1:8000

La documentation interactive Swagger est disponible à l'adresse :

http://127.0.0.1:8000/docs

5.2. Documentation des endpoints

La documentation Swagger permet de consulter les endpoints disponibles, les méthodes HTTP, les paramètres attendus, les schémas de données et les réponses de l'API.

Les principaux endpoints sont :

Détail des endpoints

- `GET /` : retourne un message confirmant que l'API fonctionne.
- `GET /health` : retourne un statut indiquant que l'application est opérationnelle.
- `POST /predict` : reçoit les 32 caractéristiques d'un employé, vérifie les données avec Pydantic, applique le modèle de Machine Learning et enregistre la demande ainsi que la prédiction dans PostgreSQL.

L'endpoint `/predict` nécessite une clé API transmise dans l'en-tête HTTP `X-API-Key`.

Les champs attendus et leur format doivent respecter le schéma de validation défini dans l'API.

Les réponses et les codes HTTP possibles peuvent être consultés directement dans Swagger.

5.3. Authentification dans Swagger

Pour utiliser l'endpoint de prédiction :

Démarrer l'API après avoir défini la variable d'environnement API_KEY.

Ouvrir la documentation Swagger à l'adresse http://127.0.0.1:8000/docs.

Cliquer sur le bouton Authorize.

Renseigner la clé API générée dans le terminal.

Valider avec Authorize, puis fermer la fenêtre.

Sélectionner l'endpoint POST /predict.

Renseigner les caractéristiques de l'employé conformément au schéma demandé.

Exécuter la requête.

Consulter la réponse contenant la prédiction.

La clé est transmise dans l'en-tête HTTP X-API-Key. Elle n'est pas intégrée au corps JSON de la requête.

5.4. Exemple d'utilisation

**Exemple de requête POST /predict**

En-tête HTTP :

`X-API-Key: votre_cle_api`

Corps de la requête :

```json
{
  "age": 30,
  "revenu_mensuel": 5000,
  "nombre_experiences_precedentes": 2,
  "nombre_heures_travailless": 40,
  "annee_experience_totale": 8,
  "annees_dans_l_entreprise": 3,
  "annees_dans_le_poste_actuel": 2,
  "satisfaction_employee_environnement": 3,
  "note_evaluation_precedente": 3,
  "niveau_hierarchique_poste": 2,
  "satisfaction_employee_nature_travail": 3,
  "satisfaction_employee_equipe": 3,
  "satisfaction_employee_equilibre_pro_perso": 3,
  "note_evaluation_actuelle": 3,
  "heure_supplementaires": "Oui",
  "augementation_salaire_precedente": 10,
  "nombre_participation_pee": 1,
  "nb_formations_suivies": 2,
  "nombre_employee_sous_responsabilite": 0,
  "niveau_education": 3,
  "domaine_etude": "Marketing",
  "frequence_deplacement": "Occasionnel",
  "annees_depuis_la_derniere_promotion": 1,
  "annes_sous_responsable_actuel": 2,
  "anciennete_avant_entreprise": 1,
  "ratio_anciennete_poste": 0.5,
  "temps_sans_promotion": 1,
  "distance_domicile_travail": 10,
  "genre": "F",
  "statut_marital": "Célibataire",
  "departement": "Commercial",
  "poste": "Consultant"
}
```

**Exemple de réponse :**

```json
{
  "prediction": 1
}
```

5.5. Gestion des erreurs d'authentification

L'API vérifie la présence et la validité de la clé API avant d'autoriser l'accès à l'endpoint /predict.

Les réponses suivantes ont été vérifiées :

200 OK : la clé API est valide et la prédiction est exécutée.

401 Unauthorized : la clé API est absente ou invalide.

422 Unprocessable Entity : les données transmises ne respectent pas le schéma de validation.

500 Internal Server Error : une erreur interne empêche le traitement de la demande.

Lorsqu'aucune clé API n'est configurée côté serveur, l'API retourne une erreur de configuration plutôt que d'autoriser une requête non protégée.

6. Base de données PostgreSQL

Le projet utilise PostgreSQL pour stocker les données des employés, les demandes envoyées à l'API et les résultats produits par le modèle.

Les tables utilisées sont :

employees : contient les données du dataset RH.

prediction_requests : conserve les données envoyées à l'API.

prediction_results : conserve les prédictions associées aux demandes.

SQLAlchemy est utilisé pour gérer les interactions entre Python et la base de données.

Le schéma et les relations entre les tables sont documentés dans schema_bdd.md.

6.1. Création des tables

Pour créer les tables définies dans les modèles SQLAlchemy :

python -m src.create_db

6.2. Chargement des données des employés

La table employees contient 1 470 employés issus du jeu de données RH.

Les données présentes dans PostgreSQL ont été exportées au format CSV afin de conserver une copie et de permettre de reproduire le chargement dans une base de données vide.

Attention : le fichier d'export contient des données RH. Il doit rester local et ne doit pas être publié sur GitHub ni intégré à une archive distribuée sans anonymisation et autorisation appropriées.

Exporter les données depuis PostgreSQL

Depuis le terminal, se connecter à la base :

psql -d projet5

Exécuter ensuite la commande SQL suivante :

\copy employees TO 'employees_export.csv' WITH CSV HEADER;

Cette commande exporte les lignes de la table employees dans le fichier employees_export.csv, avec les noms des colonnes.

Pour quitter PostgreSQL :

\q

Vérifier le fichier CSV

Le fichier d'export contient notamment les colonnes suivantes :

id_employee

age

genre

revenu_mensuel

statut_marital

departement

poste

nombre_experiences_precedentes

nombre_heures_travaillees

annee_experience_totale

annees_dans_l_entreprise

annees_dans_le_poste_actuel

La lecture du fichier avec Pandas permet de vérifier le nombre de lignes et les colonnes :

import pandas as pd

df = pd.read_csv("employees_export.csv")

print("Nombre de lignes :", len(df))
print("Colonnes :", df.columns.tolist())

Script d'importation

Le fichier src/import_employees.py permet d'importer les données du fichier CSV dans la table employees.

Pour lancer le script :

python -m src.import_employees

Le script vérifie au préalable si la table contient déjà des employés. Si des données sont présentes, l'importation est annulée afin d'éviter la création de doublons.

Dans la base principale actuelle, les 1 470 employés sont déjà enregistrés. Le script n'a donc pas été exécuté pour les insérer une seconde fois.

Vérification dans PostgreSQL

Pour vérifier le nombre d'employés enregistrés :

SELECT COUNT(*) FROM employees;

Résultat constaté dans la base principale : 1470.

Cette procédure permet de vérifier les données présentes dans la table et de documenter la préparation de leur importation dans une base vide.

6.3. Enregistrement des demandes et des prédictions

Lorsqu'une requête est envoyée à l'API FastAPI, les données transmises sont enregistrées dans la table prediction_requests.

La prédiction produite par le modèle est ensuite enregistrée dans la table prediction_results.

Chaque résultat est associé à sa demande grâce à la clé étrangère request_id.

6.4. Consultation des demandes et des prédictions

Pour consulter les demandes et les prédictions associées, la requête SQL suivante peut être exécutée :

SELECT
    pr.id AS demande_id,
    pr.input_data AS donnees_envoyees,
    res.prediction AS prediction_obtenue,
    pr.created_at AS date_demande
FROM prediction_requests pr
JOIN prediction_results res
    ON pr.id = res.request_id
ORDER BY pr.id DESC
LIMIT 3;

Cette requête permet de consulter les données envoyées à l'API, les prédictions obtenues et les dates d'enregistrement.

Les vérifications effectuées dans PostgreSQL ont confirmé que les demandes et les résultats correspondants sont enregistrés et associés.

7. Tests automatisés et couverture

Les tests automatisés sont réalisés avec Pytest afin de vérifier le bon fonctionnement de l'API et des fonctionnalités du projet.

7.1. Exécuter les tests

Pour lancer l'ensemble des tests :

python -m pytest -v src/tests/

Pour lancer uniquement les tests de l'API :

python -m pytest -v src/tests/test_api.py

7.2. Mesurer la couverture

Pour obtenir un rapport de couverture dans le terminal :

python -m pytest --cov=src --cov-report=term-missing

Pour générer également un rapport HTML :

python -m pytest --cov=src --cov-report=html

Le rapport HTML est généré dans le dossier htmlcov/.

7.3. Isolation des tests

Les tests sont exécutés avec une base PostgreSQL dédiée afin d'éviter de modifier les données de la base principale.

La variable DATABASE_URL permet de sélectionner la base utilisée pendant l'exécution des tests.

Exemple :

DATABASE_URL="postgresql+psycopg://localhost/projet5_test" python -m pytest -v src/tests/

Cette séparation permet de limiter les risques d'altération des données principales lors des tests.

8. Authentification, sécurité et confidentialité

La sécurité concerne à la fois l'accès à l'API, la connexion PostgreSQL, la gestion des identifiants et la protection des données RH.

8.1. Configuration des connexions

La connexion à PostgreSQL est configurée à l'aide de la variable d'environnement DATABASE_URL.

Cette méthode évite d'inscrire directement les identifiants de connexion dans le code source.

Les informations sensibles doivent être conservées dans des variables d'environnement ou dans un gestionnaire de secrets adapté.

Le fichier .env est exclu du suivi Git grâce au .gitignore.

8.2. Protection du dépôt Git

Le fichier .gitignore exclut notamment :

.venv/

__pycache__/

.coverage

.pytest_cache/

htmlcov/

.env

.env.*

.DS_Store

__MACOSX/

*.pyc

employees_export.csv

Ces exclusions évitent d'ajouter au dépôt les fichiers temporaires, les environnements locaux et l'export RH.

L'ajout d'une règle dans .gitignore ne supprime toutefois pas un fichier déjà suivi par Git. Il est donc nécessaire de vérifier régulièrement les fichiers suivis et l'historique du dépôt.

8.3. Gestion des secrets dans GitHub Actions

Le workflow CI utilise des identifiants dédiés au service PostgreSQL temporaire de test.

Aucun secret de dépôt GitHub n'est actuellement configuré.

Les identifiants de test sont réservés à l'environnement temporaire du workflow et ne doivent pas être réutilisés pour une base réelle.

Pour un futur environnement de production, les identifiants devront être placés dans des secrets GitHub ou dans un gestionnaire de secrets adapté. Ils ne devront jamais être inscrits directement dans les fichiers du dépôt.

La clé API utilisée localement est également fournie par une variable d'environnement nommée API_KEY. Elle n'est pas écrite en dur dans le code source.

8.4. Authentification et contrôle d'accès à l'API

L'API utilise un mécanisme d'authentification par clé API pour protéger l'endpoint de prédiction POST /predict.

La clé est définie dans une variable d'environnement :

API_KEY

La vérification est effectuée à chaque requête à l'aide de l'en-tête HTTP :

X-API-Key

Le mécanisme repose sur le composant APIKeyHeader de FastAPI et sur une comparaison sécurisée des clés avec secrets.compare_digest.

Le fonctionnement est le suivant :

Le client transmet une requête vers /predict.

Il ajoute la clé API dans l'en-tête X-API-Key.

L'API récupère la clé attendue depuis la variable d'environnement API_KEY.

Elle compare la clé reçue avec la clé attendue.

Si la clé est valide, la requête est autorisée et la prédiction est exécutée.

Si la clé est absente ou incorrecte, l'API retourne une réponse HTTP 401 Unauthorized.

Si la variable API_KEY n'est pas configurée côté serveur, l'API retourne une erreur de configuration HTTP 500 afin de ne pas fonctionner sans le paramètre de sécurité attendu.

Les routes / et /health restent accessibles sans clé API afin de permettre de vérifier le fonctionnement de l'application.

Le fonctionnement de cette protection a été vérifié depuis Swagger :

une requête avec une clé valide retourne une prédiction avec le code HTTP 200 ;

une requête sans clé retourne le code HTTP 401 Unauthorized.

Cette authentification par clé API constitue une protection adaptée à la démonstration locale du projet. Pour une mise en production, elle devra être complétée par HTTPS, une gestion sécurisée et renouvelable des clés, ainsi qu'un contrôle d'accès adapté aux utilisateurs.

8.5. Accès à PostgreSQL

L'accès à PostgreSQL dépend des mécanismes de connexion et des droits configurés sur le serveur PostgreSQL.

La connexion utilisée par l'application est paramétrée par DATABASE_URL.

Pour un environnement réel, il est recommandé d'utiliser un compte dédié à l'application, avec uniquement les permissions nécessaires à son fonctionnement.

La configuration locale actuelle utilise une connexion PostgreSQL sur la machine de développement. Elle ne constitue pas à elle seule une politique complète de gestion des utilisateurs et des permissions pour un serveur de production.

8.6. Confidentialité des données RH

Les données RH peuvent contenir des informations personnelles. Leur traitement doit respecter les principes de confidentialité et de limitation des accès.

Les bonnes pratiques à appliquer sont :

limiter l'accès aux données aux personnes autorisées ;

éviter de publier des données RH réelles dans le dépôt Git ;

ne pas inclure les exports contenant des données personnelles dans les archives de livraison ;

utiliser des données anonymisées ou fictives pour les démonstrations lorsque cela est possible ;

protéger les identifiants de connexion ;

limiter les informations sensibles présentes dans les journaux et les messages d'erreur.

Le fichier employees_export.csv est exclu du suivi Git afin de ne pas publier l'export des données RH.

9. Modèle de Machine Learning

Le modèle permet de réaliser des prédictions à partir des données des employés.

Il est sauvegardé dans le fichier model.joblib, puis chargé par l'API FastAPI afin de produire des prédictions à partir des données reçues.

Le modèle doit recevoir les variables attendues dans le même format que celui utilisé lors de son entraînement. Les données doivent être préparées de manière cohérente afin d'éviter les erreurs lors de la prédiction.

9.1. Fonctionnement du modèle

Le fonctionnement général est le suivant :

L'utilisateur transmet les caractéristiques d'un employé à l'API.

FastAPI vérifie les données reçues à l'aide des schémas de validation.

L'authentification par clé API est vérifiée pour l'endpoint de prédiction.

Les données sont transmises au modèle de Machine Learning.

Le modèle produit une prédiction.

La demande et le résultat sont enregistrés dans PostgreSQL.

L'API retourne la réponse à l'utilisateur.

La signification des classes prédites doit être interprétée selon le codage réel de la variable cible du modèle.

9.2. Maintenance et suivi des performances

Le modèle doit être évalué régulièrement à partir de nouvelles données représentatives.

Les prédictions obtenues doivent être comparées aux résultats réels lorsque ceux-ci sont disponibles. Les métriques d'évaluation doivent ensuite être comparées à celles du modèle actuel afin de détecter une éventuelle baisse de performance.

9.3. Choix techniques

Scikit-learn : entraînement et utilisation du modèle de Machine Learning.

Joblib : sauvegarde et chargement du modèle dans model.joblib.

FastAPI : mise à disposition du modèle via une API.

SQLAlchemy : gestion des interactions avec PostgreSQL.

PostgreSQL : stockage des données.

Pytest : vérification du bon fonctionnement de l'API et des fonctionnalités.

GitHub Actions : automatisation des vérifications du code.

Ces outils permettent de séparer le modèle, l'API, la base de données et les tests, et facilitent la maintenance du projet.

10. Architecture du projet

L'organisation générale du projet est la suivante :

projet-5-data-scientist/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── src/
│   ├── api.py
│   ├── models.py
│   ├── database.py
│   ├── create_db.py
│   ├── import_employees.py
│   └── tests/
│       ├── test_api.py
│       └── test_import_employees.py
│
├── model.joblib
├── requirements.txt
├── README.md
├── schema_bdd.md
└── .gitignore

Principaux fichiers :

src/api.py : gestion de l'API FastAPI, de l'authentification et des prédictions.

src/models.py : définition des modèles de données SQLAlchemy.

src/database.py : configuration de la connexion à PostgreSQL.

src/create_db.py : création des tables de la base de données.

src/import_employees.py : importation des employés dans PostgreSQL, avec vérification pour éviter les doublons.

src/tests/ : tests automatisés du projet.

model.joblib : modèle de Machine Learning sauvegardé.

requirements.txt : dépendances Python du projet.

schema_bdd.md : documentation du schéma de la base de données.

.github/workflows/ci.yml : configuration du workflow d'intégration continue.

Le fichier employees_export.csv est un export local de données RH. Il n'est pas inclus dans le dépôt Git ni dans l'architecture de livraison afin de protéger les données des employés.

11. Maintenance et mise à jour du modèle

11.1. Vérification des performances

Le modèle doit être évalué régulièrement à partir de nouvelles données représentatives.

Les prédictions obtenues doivent être comparées aux résultats réels lorsque ceux-ci sont disponibles. Les métriques d'évaluation doivent ensuite être comparées à celles du modèle actuel afin de détecter une éventuelle baisse de performance.

11.2. Réentraînement du modèle

Si les performances diminuent ou si les données évoluent, le modèle peut être réentraîné avec des données récentes et correctement préparées.

Les mêmes étapes de préparation des données et la même méthode d'évaluation doivent être conservées afin de comparer les résultats de manière cohérente.

11.3. Tests du nouveau modèle

Avant son remplacement, le nouveau modèle doit être évalué sur un jeu de test indépendant.

Il faut vérifier ses performances, s'assurer qu'il accepte les données attendues et exécuter les tests de l'API :

./.venv/bin/python -m pytest

Le nouveau modèle ne doit être retenu que si les tests passent et si ses performances sont satisfaisantes.

11.4. Remplacement du modèle

Conserver une copie de sauvegarde de l'ancien fichier model.joblib.

Enregistrer le nouveau modèle au format Joblib sous le nom model.joblib.

Remplacer l'ancien fichier par le nouveau dans le projet.

Redémarrer l'API.

Vérifier que les prédictions fonctionnent correctement.

Exécuter les tests automatisés afin de vérifier que le remplacement n'a pas introduit de régression.

**Validation des données et gestion des cas limites**

Les tests vérifient le comportement de l'API face à différentes entrées :

- Acceptation d'un âge égal à la limite minimale autorisée (18 ans).
- Rejet des âges négatifs et des âges supérieurs à 65 ans.
- Rejet des requêtes lorsque des champs obligatoires sont manquants.
- Rejet des notes de satisfaction situées en dehors de l'intervalle autorisé.
- Rejet des catégories non reconnues, comme une valeur de genre différente de « F » ou « M ».

Les données invalides sont rejetées avec un code HTTP `422`.

**Vérification des limites numériques**

Les tests automatisés contrôlent également les valeurs minimales autorisées pour les caractéristiques des employés.

Ils vérifient notamment :

- Le rejet des notes de satisfaction et d'évaluation égales à 0.
- Le rejet des niveaux hiérarchiques et d'éducation égaux à 0.
- Le rejet des valeurs négatives pour les variables numériques : revenu, expérience, heures travaillées, ancienneté, formations, promotions et autres caractéristiques.

Ces contrôles permettent de vérifier que les contraintes définies dans les schémas Pydantic sont bien appliquées par l'API. Les entrées non conformes renvoient un code HTTP `422`.

**Résultats des tests automatisés**

Les tests du fichier `src/tests/test_api.py` ont été exécutés avec Pytest.

Résultat : **18 tests réussis en 3,35 secondes (18 passed)**.

Les tests couvrent notamment :
- Le fonctionnement des endpoints de l'API.
- L'authentification par clé API.
- La validation des données d'entrée.
- Les cas limites et les valeurs incorrectes.
- Le fonctionnement de la création des tables PostgreSQL.
- Le format de la prédiction retournée.


**Couverture des tests**

La couverture des tests a été mesurée avec Coverage.py.

La couverture globale du projet est de **77 %**, sur 318 instructions analysées, dont 72 ne sont pas couvertes.

Les résultats montrent notamment :
- `src/database.py` : 100 %
- `src/import_employees.py` : 95 %
- `src/models.py` : 100 %
- `src/tests/test_api.py` : 71 %
- `src/tests/test_example.py` : 100 %
- `src/tests/test_import_employees.py` : 94 %

Commande utilisée :

```bash
./.venv/bin/python -m coverage report
```

**Générer un rapport détaillé**

Pour générer un rapport HTML permettant d'identifier les lignes de code couvertes ou non couvertes par les tests :

```bash
./.venv/bin/python -m coverage html
```

Le rapport est généré dans le dossier `htmlcov/`. Il peut être consulté en ouvrant le fichier `htmlcov/index.html` dans un navigateur.

### Analyse de l'importance des variables

Le modèle Random Forest permet d'examiner l'importance relative des variables utilisées dans ses prédictions.

Après transformation des données par le pipeline de prétraitement (`StandardScaler` et `OneHotEncoder`), le modèle utilise 53 variables transformées.

Les variables présentant les importances les plus élevées sont notamment :

- Âge : 7,22 %
- Revenu mensuel : 7,22 %
- Expérience professionnelle totale : 5,55 %
- Distance domicile-travail : 4,65 %
- Ratio ancienneté/poste : 3,77 %

Ces importances permettent d'identifier les variables qui contribuent le plus aux décisions du modèle. Elles ne constituent pas des métriques de performance et ne permettent pas, à elles seules, d'évaluer la qualité des prédictions.