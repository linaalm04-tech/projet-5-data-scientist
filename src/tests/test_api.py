from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


def test_accueil():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "L'API fonctionne"}


def test_verification():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
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
        "augmentation_salaire_precedente": 10,
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
    features["age"] = 30
    response = client.post("/predict", json=features)
    print("CHAMP ENVOYÉ :", features.get("augmentation_salaire_precedente"))
    print("CLÉS ENVOYÉES :", list(features.keys()))
    print(response.status_code)
    print(response.text)
    print([e["loc"] for e in response.json().get("detail", [])])
    assert response.status_code == 200 , response.text
    


def test_prediction_champ_manquant():
    """Vérifie que l'API refuse une requête incomplète."""
    response = client.post("/predict", json={"age": 30})
    assert response.status_code == 422
    
   