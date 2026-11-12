"""Persistence operations for model predictions."""

from sqlalchemy import Engine, text
from sqlalchemy.dialects.postgresql import insert as postgresql_insert
from sqlalchemy.orm import Session

from VLRRatingCalculatorDB.dto.prediction_info import PredictionInput
from VLRRatingCalculatorDB.model.prediction import PredictionModel


class PredictionRepository:
    """Create the prediction table and upsert each match/model-version slot."""

    UNIQUE_CONSTRAINT = "uq_predictions_model_version_match_variant"
    UNIQUE_COLUMNS = {
        "vlr_match_id",
        "evaluation_year",
        "model_type",
        "model_name",
        "model_version",
        "training_style",
        "feature_set",
        "run_label",
    }

    def create_table(self, engine: Engine) -> None:
        """Create the table and migrate to version-aware prediction upserts."""
        PredictionModel.__table__.create(engine, checkfirst=True)
        with engine.begin() as connection:
            connection.execute(
                text(
                    "ALTER TABLE predictions "
                    "ADD COLUMN IF NOT EXISTS model_version VARCHAR(10) "
                    "NOT NULL DEFAULT 'V3'"
                )
            )
            connection.execute(
                text(
                    "ALTER TABLE predictions "
                    "ALTER COLUMN model_version SET DEFAULT 'V3'"
                )
            )
            connection.execute(
                text(
                    "UPDATE predictions SET model_version = 'V1' "
                    "WHERE model_version IS NULL OR btrim(model_version) = ''"
                )
            )
            connection.execute(
                text(
                    "DO $$ BEGIN "
                    "IF EXISTS ("
                    "SELECT 1 FROM pg_constraint "
                    "WHERE conrelid = 'predictions'::regclass "
                    "AND conname = 'uq_predictions_run_match_variant'"
                    ") THEN "
                    "ALTER TABLE predictions "
                    "DROP CONSTRAINT uq_predictions_run_match_variant; "
                    "END IF; "
                    "IF NOT EXISTS ("
                    "SELECT 1 FROM pg_constraint "
                    "WHERE conrelid = 'predictions'::regclass "
                    "AND conname = 'uq_predictions_model_version_match_variant'"
                    ") THEN "
                    "ALTER TABLE predictions "
                    "ADD CONSTRAINT uq_predictions_model_version_match_variant "
                    "UNIQUE (vlr_match_id, evaluation_year, model_type, model_name, "
                    "model_version, training_style, feature_set, run_label); "
                    "END IF; "
                    "END $$"
                )
            )

    def insert_predictions(
        self,
        predictions_data: list[PredictionInput],
        session: Session | None,
        commit: bool = True,
        batch_size: int = 500,
    ) -> int:
        """Upsert prediction rows, returning the number of rows processed."""
        if session is None:
            raise ValueError("Session is None. Please provide a valid session.")
        if batch_size < 1:
            raise ValueError("batch_size must be positive")
        if not predictions_data:
            return 0

        rows = [prediction.model_dump(mode="python") for prediction in predictions_data]
        insert_statement = postgresql_insert(PredictionModel)
        update_columns = {
            column.name: getattr(insert_statement.excluded, column.name)
            for column in PredictionModel.__table__.columns
            if column.name not in self.UNIQUE_COLUMNS | {"id", "created_at"}
        }

        try:
            for offset in range(0, len(rows), batch_size):
                batch = rows[offset : offset + batch_size]
                statement = insert_statement.values(batch).on_conflict_do_update(
                    constraint=self.UNIQUE_CONSTRAINT,
                    set_=update_columns,
                )
                session.execute(statement)

            if commit:
                session.commit()
            else:
                session.flush()
        except Exception:
            if commit:
                session.rollback()
            raise

        return len(rows)
