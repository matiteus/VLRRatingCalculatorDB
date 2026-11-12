"""ORM model for saved model predictions linked to VLR matches."""

import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from VLRRatingCalculatorDB.model.base import Base
from VLRRatingCalculatorDB.model.match import MatchModel


class PredictionModel(Base):
    """One saved prediction per match, fold, model version, and variant."""

    __tablename__ = "predictions"
    __table_args__ = (
        UniqueConstraint(
            "vlr_match_id",
            "evaluation_year",
            "model_type",
            "model_name",
            "model_version",
            "training_style",
            "feature_set",
            "run_label",
            name="uq_predictions_model_version_match_variant",
        ),
        CheckConstraint(
            "training_style IN ('yearly', 'progressive')",
            name="ck_predictions_training_style",
        ),
        CheckConstraint(
            "team_a_win_probability >= 0 AND team_a_win_probability <= 1",
            name="ck_predictions_team_a_probability_range",
        ),
        CheckConstraint(
            "team_b_win_probability >= 0 AND team_b_win_probability <= 1",
            name="ck_predictions_team_b_probability_range",
        ),
        CheckConstraint(
            "decision_threshold >= 0 AND decision_threshold <= 1",
            name="ck_predictions_decision_threshold_range",
        ),
        CheckConstraint(
            "training_rows > 0",
            name="ck_predictions_training_rows_positive",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vlr_match_id: Mapped[int] = mapped_column(
        ForeignKey("val_matches.vlr_match_id", ondelete="CASCADE"),
        nullable=False,
    )
    prediction_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    evaluation_year: Mapped[int] = mapped_column(Integer, nullable=False)
    model_type: Mapped[str] = mapped_column(String(50), nullable=False)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    model_version: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="V3",
        server_default=text("'V3'"),
    )
    training_style: Mapped[str] = mapped_column(String(30), nullable=False)
    feature_set: Mapped[str] = mapped_column(String(100), nullable=False)
    uses_glicko: Mapped[bool] = mapped_column(Boolean, nullable=False)
    run_label: Mapped[str] = mapped_column(String(100), nullable=False)
    mlflow_experiment_name: Mapped[str] = mapped_column(String(200), nullable=False)
    mlflow_run_id: Mapped[str] = mapped_column(String(100), nullable=False)
    mlflow_run_name: Mapped[str] = mapped_column(String(255), nullable=False)
    training_start_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    training_end_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    training_rows: Mapped[int] = mapped_column(Integer, nullable=False)
    team_a: Mapped[str] = mapped_column(String, nullable=False)
    team_b: Mapped[str] = mapped_column(String, nullable=False)
    team_a_win_probability: Mapped[float] = mapped_column(Float, nullable=False)
    team_b_win_probability: Mapped[float] = mapped_column(Float, nullable=False)
    predicted_team_a_win: Mapped[bool] = mapped_column(Boolean, nullable=False)
    actual_team_a_win: Mapped[bool] = mapped_column(Boolean, nullable=False)
    predicted_winner: Mapped[str] = mapped_column(String, nullable=False)
    actual_winner: Mapped[str] = mapped_column(String, nullable=False)
    correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    decision_threshold: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
