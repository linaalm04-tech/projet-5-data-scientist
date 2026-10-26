
from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
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
