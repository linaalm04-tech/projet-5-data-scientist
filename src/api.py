from pathlib import Path
from typing import Optional
import os
import secrets
from pydantic import BaseModel, Field
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Depends, Security
from src.database import SessionLocal
from src.models import PredictionRequest, PredictionResult
from fastapi.security import APIKeyHeader

MODEL_PATH = Path(__file__).resolve().parent.parent / "model.joblib"
model = joblib.load(MODEL_PATH)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verifier_cle_api(api_key: Optional[str] = Security(api_key_header)):
    cle_attendue = os.getenv("API_KEY")

    if not cle_attendue:
        raise HTTPException(
            status_code=500,
            detail="La configuration de sécurité de l'API est absente."
        )

    if not api_key or not secrets.compare_digest(api_key, cle_attendue):
        raise HTTPException(
            status_code=401,
            detail="Clé API manquante ou invalide."
        )


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
    age: int = Field(ge=18, le=65)
    genre: Literal["F", "M"]
    revenu_mensuel: float = Field(ge=0)
    statut_marital: Literal["Célibataire", "Divorcé(e)", "Marié(e)"]
    departement: Literal["Commercial", "Consulting", "Ressources Humaines"]
    poste: Literal[
    "Assistant de Direction",
    "Cadre Commercial",
    "Consultant",
    "Directeur Technique",
    "Manager",
    "Représentant Commercial",
    "Ressources Humaines",
    "Senior Manager",
    "Tech Lead"
]
    nombre_experiences_precedentes: int = Field(ge=0)
    nombre_heures_travailless: int = Field(ge=0)
    annee_experience_totale: int = Field(ge=0)
    annees_dans_l_entreprise: int = Field(ge=0)
    annees_dans_le_poste_actuel: int = Field(ge=0)
    satisfaction_employee_environnement: int = Field(ge=1, le=4)
    note_evaluation_precedente: int = Field(ge=1, le=4)
    niveau_hierarchique_poste: int = Field(ge=1, le=5)
    satisfaction_employee_nature_travail: int = Field(ge=1, le=4)
    satisfaction_employee_equipe: int = Field(ge=1, le=4)
    satisfaction_employee_equilibre_pro_perso: int = Field(ge=1, le=4)
    note_evaluation_actuelle: int = Field(ge=1, le=4)
    heure_supplementaires: Literal["Non", "Oui"]
    augementation_salaire_precedente: float = Field(ge=0)
    nombre_participation_pee: int = Field(ge=0)
    nb_formations_suivies: int = Field(ge=0)
    nombre_employee_sous_responsabilite: int = Field(ge=0)
    niveau_education: int = Field(ge=1, le=5)
    domaine_etude: Literal[
    "Autre",
    "Entrepreunariat",
    "Infra & Cloud",
    "Marketing",
    "Ressources Humaines",
    "Transformation Digitale"
    ]
    frequence_deplacement: Literal["Aucun", "Frequent", "Occasionnel"]
    annees_depuis_la_derniere_promotion: int = Field(ge=0)
    annes_sous_responsable_actuel: int = Field(ge=0)
    anciennete_avant_entreprise: int = Field(ge=0)
    ratio_anciennete_poste: float = Field(ge=0)
    temps_sans_promotion: int = Field(ge=0)
    distance_domicile_travail: int = Field(ge=0)
@app.post("/predict", dependencies=[Depends(verifier_cle_api)])
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

    except HTTPException:
      session.rollback()
      raise

    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Une erreur interne est survenue lors de la prédiction."
        ) from None

    finally:
     session.close()

        
    
