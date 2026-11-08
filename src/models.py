
from sqlalchemy import Column, Integer, DateTime, ForeignKey, func, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from src.database import Base


class PredictionRequest(Base):
    __tablename__ = "prediction_requests"

    id = Column(Integer, primary_key=True, index=True)
    input_data = Column(JSONB, nullable=False)
    created_at = Column(
        DateTime,
        server_default=func.current_timestamp(),
        nullable=False,
    )

    result = relationship(
        "PredictionResult",
        back_populates="request",
        uselist=False,
    )


class PredictionResult(Base):
    __tablename__ = "prediction_results"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(
        Integer,
        ForeignKey("prediction_requests.id"),
        nullable=False,
        unique=True,
    )
    prediction = Column(Integer, nullable=False)
    created_at = Column(
        DateTime,
        server_default=func.current_timestamp(),
        nullable=False,
    )

    request = relationship(
        "PredictionRequest",
        back_populates="result",
    )

class Employee(Base):
    __tablename__ = "employees"

    id_employee = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=True)
    genre = Column(Text, nullable=True)
    revenu_mensuel = Column(Integer, nullable=True)
    statut_marital = Column(Text, nullable=True)
    departement = Column(Text, nullable=True)
    poste = Column(Text, nullable=True)
    nombre_experiences_precedentes = Column(Integer, nullable=True)
    nombre_heures_travaillees = Column(Integer, nullable=True)
    annee_experience_totale = Column(Integer, nullable=True)
    annees_dans_l_entreprise = Column(Integer, nullable=True)
    annees_dans_le_poste_actuel = Column(Integer, nullable=True)