from pathlib import Path
import joblib
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline

def main():
    data = load_dataset("deepset/prompt-injections")
    train, test = data["train"], data["test"]
    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2)),
        ("classifier", LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)),
    ])
    model.fit(train["text"], train["label"])
    predictions = model.predict(test["text"])
    print(classification_report(test["label"], predictions, target_names=["SAFE", "BLOCKED"], zero_division=0))
    print("Confusion matrix:\n", confusion_matrix(test["label"], predictions))
    output = Path(__file__).resolve().parent / "models" / "promptguard_baseline.joblib"
    output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output)
    print(f"Saved: {output}")

if __name__ == "__main__":
    main()
