from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    unzip_data_dir: Path
    all_schema: dict


@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    preprocessor_name: str
    target_column: str


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    model_name: str
    n_estimators: int
    num_leaves: int
    learning_rate: float
    max_depth: int
    target_column: str



@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path
    model_path: Path
    all_params: dict
    metric_file_name: Path
    target_column: str
    mlflow_uri: str
    registered_model_name: str  # Added for specifying MLflow model registration
    experiment_name: str  # Added to track different MLflow experiments
    run_name: str  # Optional: Naming specific runs in MLflow
    save_local_metrics: bool  # Boolean flag to save metrics locally as JSON
    confusion_matrix_file: Path  # New attribute for confusion matrix file path
    roc_curve_file: Path


# @dataclass(frozen=True)
# class ModelEvaluationConfig:
#     root_dir: Path
#     test_data_path: Path
#     model_path: Path
#     all_params: dict
#     metric_file_name: Path
#     target_column: str
#     mlflow_uri: str
#     confusion_matrix_file: str
#     roc_curve_file: str