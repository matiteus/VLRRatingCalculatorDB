"""Pydantic schemas for persisted match predictions."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    """A model prediction and the fold/run metadata needed to audit it."""

    vlr_match_id: int
    prediction_date: datetime
    evaluation_year: int
    model_type: str
    model_name: str
    model_version: Literal["V1", "V2", "V3"] = "V3"
    training_style: Literal["yearly", "progressive"]
    feature_set: str
    uses_glicko: bool
    run_label: str
    mlflow_experiment_name: str
    mlflow_run_id: str
    mlflow_run_name: str
    training_start_date: datetime
    training_end_date: datetime
    training_rows: int = Field(ge=1)
    team_a: str
    team_b: str
    team_a_win_probability: float = Field(ge=0, le=1)
    team_b_win_probability: float = Field(ge=0, le=1)
    predicted_team_a_win: bool
    actual_team_a_win: bool
    predicted_winner: str
    actual_winner: str
    correct: bool
    decision_threshold: float = Field(ge=0, le=1)
