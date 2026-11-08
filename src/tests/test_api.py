import os
from fastapi.testclient import TestClient
from src.api import app

os.environ["API_KEY"] = "test-api-key"
client = TestClient(app, headers={"X-API-Key": "test-api-key"})
def obtenir_features_valides():
    return {
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
        "poste": "Consultant",
    }


def test_accueil():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "L'API fonctionne"}


def test_verification():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_prediction_sans_cle_api():
    client_sans_cle = TestClient(app)
    response = client_sans_cle.post(
        "/predict",
        json=obtenir_features_valides()
    )
    assert response.status_code == 401

def test_api_key_absente_de_configuration(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)

    response = client.post(
        "/predict",
        json=obtenir_features_valides()
    )

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "La configuration de sécurité de l'API est absente."
    )

def test_prediction_rollback_http_exception(monkeypatch):
    from fastapi import HTTPException

    class FausseSession:
        def __init__(self):
            self.rollback_effectue = False

        def add(self, objet):
            pass

        def flush(self):
            raise HTTPException(
                status_code=400,
                detail="Erreur de test"
            )

        def rollback(self):
            self.rollback_effectue = True

        def close(self):
            pass

    session_test = FausseSession()

    monkeypatch.setattr(
        "src.api.SessionLocal",
        lambda: session_test
    )

    response = client.post(
        "/predict",
        json=obtenir_features_valides()
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Erreur de test"
    assert session_test.rollback_effectue is True



def test_prediction_rollback_erreur_interne(monkeypatch):
    class FausseSession:
        def __init__(self):
            self.rollback_effectue = False

        def add(self, objet):
            pass

        def flush(self):
            pass

        def rollback(self):
            self.rollback_effectue = True

        def close(self):
            pass

    session_test = FausseSession()



    def prediction_en_erreur(donnees):
        raise RuntimeError("Erreur simulée")

    monkeypatch.setattr(
        "src.api.SessionLocal",
        lambda: session_test
    )
    monkeypatch.setattr(
        "src.api.model.predict",
        prediction_en_erreur
    )

    response = client.post(
        "/predict",
        json=obtenir_features_valides()
    )

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "Une erreur interne est survenue lors de la prédiction."
    )
    assert session_test.rollback_effectue is True


def test_prediction_entree_incorrecte():
        response = client.post("/predict", json={})
        assert response.status_code == 422
def test_prediction():
    features = {
        "age": 30,
        "revenu_mensuel": 5000,
        "nombre_experiences_precedentes": 2,
        "augementation_salaire_precedente": 10,
        "annes_sous_responsable_actuel": 2,
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
        "nombre_participation_pee": 1,
        "nb_formations_suivies": 2,
        "nombre_employee_sous_responsabilite": 0,
        "distance_domicile_travail": 10,
        "niveau_education": 3,
        "annees_depuis_la_derniere_promotion": 1,
        "anciennete_avant_entreprise": 1,
        "ratio_anciennete_poste": 0.5,
        "temps_sans_promotion": 1,
        "genre": "F",
        "statut_marital": "Célibataire",
        "departement": "Commercial",
        "poste": "Consultant",
        "heure_supplementaires": "Oui",
        "domaine_etude": "Marketing",
        "frequence_deplacement": "Occasionnel",
    }

    response = client.post("/predict", json=features)
    import joblib
    model = joblib.load("model.joblib")
    expected = set(model.named_steps["preprocessing"].feature_names_in_)
    missing = sorted(expected - set(features.keys()))

    print("VARIABLES MANQUANTES :", missing)
    print("NOMBRE :", len(missing))

    assert not missing, f"variables manquantes : {missing}"
    print("STATUS :", response.status_code)
    print("REPONSE :", response.json())
    assert response.status_code == 200
    assert "prediction" in response.json()

def test_prediction_retourne_un_entier():
    features = {
      "age": 30,
             "revenu_mensuel": 5000,
             "nombre_experiences_precedentes": 2,
             "augementation_salaire_precedente": 10,
             "annes_sous_responsable_actuel": 2,
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
             "nombre_participation_pee": 1,
             "nb_formations_suivies": 2,
             "nombre_employee_sous_responsabilite": 0,
             "distance_domicile_travail": 10,
             "niveau_education": 3,
             "annees_depuis_la_derniere_promotion": 1,
             "anciennete_avant_entreprise": 1,
             "ratio_anciennete_poste": 0.5,
             "temps_sans_promotion": 1,
             "genre": "F",
             "statut_marital": "Célibataire",
             "departement": "Commercial",
             "poste": "Consultant",
             "heure_supplementaires": "Oui",
             "domaine_etude": "Marketing",
             "frequence_deplacement": "Occasionnel",
         }

    response = client.post("/predict", json=features)

    assert response.status_code == 200
    assert isinstance(response.json()["prediction"], int)
def test_prediction_entree_invalide():
    response = client.post(
        "/predict",
        json={"age": "texte"}
    )
    assert response.status_code == 422
def test_creer_tables(monkeypatch):
     from src import create_db

     appele = {}
     def fake_create_all(bind):
         appele["bind"] = bind
     monkeypatch.setattr(create_db.Base.metadata, "create_all", fake_create_all)
     create_db.create_tables()
     assert "bind" in appele
     assert appele["bind"] == create_db.engine


def test_prediction_age_limite():
    """Vérifie le comportement de l'API avec un âge à la limite."""
    features = {
        "age": 18,
        "revenu_mensuel": 5000,
        "nombre_experiences_precedentes": 2,
        "annes_sous_responsable_actuel": 2,
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
        "nombre_participation_pee": 1,
        "nb_formations_suivies": 2,
        "nombre_employee_sous_responsabilite": 0,
        "distance_domicile_travail": 10,
        "niveau_education": 3,
        "annees_depuis_la_derniere_promotion": 1,
        "anciennete_avant_entreprise": 1,
        "ratio_anciennete_poste": 0.5,
        "temps_sans_promotion": 1,
        "genre": "F",
        "statut_marital": "Célibataire",
        "departement": "Commercial",
        "poste": "Consultant",
        "heure_supplementaires": "Oui",
        "domaine_etude": "Marketing",
        "frequence_deplacement": "Occasionnel",
        "augementation_salaire_precedente": 0,
    }

    response = client.post("/predict", json=features)
    assert response.status_code == 200 , response.text



def test_prediction_champ_manquant():
    """Vérifie que l'API refuse une requête incomplète."""
    response = client.post("/predict", json={"age": 30})
    assert response.status_code == 422

def test_prediction_valeurs_negatives():
    features = obtenir_features_valides()
    features["age"] = -5

    response = client.post("/predict", json=features)
    assert response.status_code == 422


def test_prediction_age_superieur_limite():
    features = obtenir_features_valides()
    features["age"] = 66

    response = client.post("/predict", json=features)
    assert response.status_code == 422


def test_prediction_note_superieure_limite():
    features = obtenir_features_valides()
    features["satisfaction_employee_environnement"] = 5

    response = client.post("/predict", json=features)
    assert response.status_code == 422

def test_prediction_categorie_invalide():
    features = obtenir_features_valides()
    features["genre"] = "X"

    response = client.post("/predict", json=features)
    assert response.status_code == 422

def test_prediction_note_inferieure_limite():
    features = obtenir_features_valides()
    features["satisfaction_employee_environnement"] = 0

    response = client.post("/predict", json=features)
    assert response.status_code == 422

def test_notes_minimales():
    champs = [
        "note_evaluation_precedente",
        "satisfaction_employee_nature_travail",
        "satisfaction_employee_equipe",
        "satisfaction_employee_equilibre_pro_perso",
        "note_evaluation_actuelle",
    ]

    for champ in champs:
        features = obtenir_features_valides()
        features[champ] = 0

        response = client.post("/predict", json=features)
        assert response.status_code == 422, f"Le champ {champ} accepte 0"

def test_niveaux_minimaux():
    for champ in ["niveau_hierarchique_poste", "niveau_education"]:
        features = obtenir_features_valides()
        features[champ] = 0

        response = client.post("/predict", json=features)
        assert response.status_code == 422, f"Le champ {champ} accepte 0"

def test_champs_numeriques_refusent_valeurs_negatives():
    champs = [
        "revenu_mensuel",
        "nombre_experiences_precedentes",
        "nombre_heures_travailless",
        "annee_experience_totale",
        "annees_dans_l_entreprise",
        "annees_dans_le_poste_actuel",
        "augementation_salaire_precedente",
        "nombre_participation_pee",
        "nb_formations_suivies",
        "nombre_employee_sous_responsabilite",
        "annees_depuis_la_derniere_promotion",
        "annes_sous_responsable_actuel",
        "anciennete_avant_entreprise",
        "ratio_anciennete_poste",
        "temps_sans_promotion",
        "distance_domicile_travail",
    ]

    for champ in champs:
        features = obtenir_features_valides()
        features[champ] = -1

        response = client.post("/predict", json=features)

        assert response.status_code == 422, (
            f"Le champ {champ} accepte une valeur négative"
        )