import mlflow
import joblib
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from urllib.parse import urlparse
from dataclasses import dataclass
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    confusion_matrix, roc_curve, auc
)
import os
import json
from mlFlowProject.entity.config_entity import ModelEvaluationConfig

from dotenv import load_dotenv
load_dotenv()

os.environ["MLFLOW_TRACKING_URI"] = os.environ.get("MLFLOW_TRACKING_URI")
os.environ["MLFLOW_TRACKING_USERNAME"] = os.environ.get("MLFLOW_TRACKING_USERNAME")
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.environ.get("MLFLOW_TRACKING_PASSWORD")


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self, actual, pred):
        accuracy = accuracy_score(actual, pred)
        precision = precision_score(actual, pred)
        recall = recall_score(actual, pred)
        f1 = f1_score(actual, pred)

        return accuracy, precision, recall, f1

    def save_json(self, path: Path, data: dict):
        """Saves a dictionary as a JSON file."""
        # Ensure path is a Path object, not a string
        path = Path(path)
        path.write_text(json.dumps(data, indent=4))
   

    def log_into_mlflow(self):
        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        test_x = test_data.drop([self.config.target_column], axis=1)
        test_y = test_data[[self.config.target_column]]

        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():
            # Log tags
            mlflow.set_tag("model_version", "v1.0")
            mlflow.set_tag("experiment_name", "Model Evaluation Experiment")
            mlflow.set_tag("target_column", self.config.target_column)
            mlflow.set_tag("data_source", str(self.config.test_data_path))
            mlflow.set_tag("evaluation_time", str(datetime.datetime.now()))

            predictions = model.predict(test_x)
            accuracy, precision, recall, f1 = self.eval_metrics(test_y, predictions)

            # Saving metrics locally
            scores = {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1": f1
            }
            self.save_json(path=self.config.metric_file_name, data=scores)

            # Log metrics to MLflow
            mlflow.log_params(self.config.all_params)
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.log_metric("f1-score", f1)

            # Log confusion matrix as artifact
            cm = confusion_matrix(test_y, predictions)
            cm_file = "confusion_matrix.png"
            plt.figure(figsize=(8, 6))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                        xticklabels=['Class 0', 'Class 1'], yticklabels=['Class 0', 'Class 1'])
            plt.title("Confusion Matrix")
            plt.savefig(cm_file)
            mlflow.log_artifact(cm_file)  # Log it to MLflow
            self.save_json(path=self.config.confusion_matrix_file, data=cm.tolist())  # Optionally save locally

            # Log ROC curve as artifact
            fpr, tpr, _ = roc_curve(test_y, model.predict_proba(test_x)[:, 1])
            roc_auc = auc(fpr, tpr)
            roc_file = "roc_curve.png"
            plt.figure()
            plt.plot(fpr, tpr, color="blue", lw=2, label="ROC curve (area = %0.2f)" % roc_auc)
            plt.plot([0, 1], [0, 1], color="gray", lw=2, linestyle="--")
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel("False Positive Rate")
            plt.ylabel("True Positive Rate")
            plt.title("Receiver Operating Characteristic")
            plt.legend(loc="lower right")
            plt.savefig(roc_file)
            mlflow.log_artifact(roc_file)  # Log it to MLflow
            self.save_json(path=self.config.roc_curve_file, data={"fpr": fpr.tolist(), "tpr": tpr.tolist()})  # Optionally save locally

            # Log the model into MLflow
            if tracking_url_type_store != "file":
                mlflow.sklearn.log_model(model, "model", registered_model_name="LightGBM")
            else:
                mlflow.sklearn.log_model(model, "model")