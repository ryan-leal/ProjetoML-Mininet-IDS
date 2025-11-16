import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

DATA_PATH = "data/flows_features.csv"
MODEL_PATH = "data/model_flowguard.pkl"

def main():
    df = pd.read_csv(DATA_PATH)

    feature_cols = [
        "duration",
        "n_pkts",
        "n_bytes",
        "pkts_per_sec",
        "syn_ratio",
        "ack_ratio",
    ]

    X = df[feature_cols]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    clf = DecisionTreeClassifier(
        max_depth=4,
        class_weight="balanced",
        random_state=42,
    )

    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print("Matriz de confusão:")
    print(confusion_matrix(y_test, y_pred))
    print("\nRelatório de classificação:")
    print(classification_report(y_test, y_pred))

    joblib.dump(clf, MODEL_PATH)
    print(f"\n[+] Modelo salvo em {MODEL_PATH}")

if __name__ == "__main__":
    main()
