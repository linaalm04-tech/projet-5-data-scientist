from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.database import SessionLocal
from src.models import PredictionRequest, PredictionResult

MODEL_PATH = Path(__file__).resolve().parent.parent / "model.joblib"
model = joblib.load(MODEL_PATH)

app = FastAPI(
    title="API de prédiction",
    description="API pour exposer un modèle de machine learning",
    version="1.0.0",
)


@app.get("/")
def accueil():
    return {"message": "L'API fonctionne"}


@app.get("/health")
def verification():
    return {"status": "ok"}

class Features(BaseModel):
    age: int
    genre: str
    revenu_mensuel: float
    statut_marital: str
    departement: str
    poste: str
    nombre_experiences_precedentes: int
    nombre_heures_travailless: int
    annee_experience_totale: int
    annees_dans_l_entreprise: int
    annees_dans_le_poste_actuel: int
    satisfaction_employee_environnement: int
    note_evaluation_precedente: int
    niveau_hierarchique_poste: int
    satisfaction_employee_nature_travail: int
    satisfaction_employee_equipe: int
    satisfaction_employee_equilibre_pro_perso: int
    note_evaluation_actuelle: int
    heure_supplementaires: str
    augementation_salaire_precedente: int
    nombre_participation_pee: int
    nb_formations_suivies: int
    nombre_employee_sous_responsabilite: int
    niveau_education: int
    domaine_etude: str
    frequence_deplacement: str
    annees_depuis_la_derniere_promotion: int
    annes_sous_responsable_actuel: int
    anciennete_avant_entreprise: int
    ratio_anciennete_poste: float
    temps_sans_promotion: int
    distance_domicile_travail: int
@app.post("/predict")
def prediction(features: Features):
    session = SessionLocal()
    try:
       donnees_dict = features.model_dump()
       donnees = pd.DataFrame([donnees_dict])

       demande = PredictionRequest(input_data=donnees_dict)
       session.add(demande)
       session.flush()

       resultat = model.predict(donnees)[0]
       prediction_value = int(resultat) 
       resultat_db = PredictionResult(
            request_id=demande.id,
            prediction=prediction_value
        )
       session.add(resultat_db)
       session.commit()

       return {"prediction": prediction_value}

    except Exception as erreur:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(erreur))

    finally:
        session.close()

        
    
