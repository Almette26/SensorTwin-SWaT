"""
CP2 Baseline Implementation: PCA Reconstruction Error
Project: SensorTwin-SWaT (IC3 - SIVA)
"""

import os
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report, confusion_matrix, f1_score, precision_score, recall_score
from data_loader import SWaTDataLoader

def run_pca_baseline():
    print("=" * 60)
    print(">> [CP2] Rulare Baseline: PCA Reconstruction Error pe SWaT")
    print("=" * 60)

    # 1. Incarcare date prin pipeline-ul validat
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir, "data")
    loader = SWaTDataLoader(data_dir=dataset_path, train_split_ratio=0.75)
    X_train, y_train, X_test, y_test, features = loader.load_and_preprocess()

    # 2. Configurare si antrenare model de reprezentare liniara (PCA)
    # Selectam 14 componente (retin >80% din varianta procesului pe 44 variabile)
    n_components = 14
    print(f"\n>> Antrenare PCA cu n_components={n_components} pe {X_train.shape[0]} eșantioane normale...")
    pca = PCA(n_components=n_components, random_state=42)
    pca.fit(X_train)
    
    var_exp = np.sum(pca.explained_variance_ratio_) * 100
    print(f">> Varianta cumulata explicata: {var_exp:.2f}%")

    # 3. Calcul eroare de reconstructie (SPE)
    print(">> Calcul eroare de reconstructie pe Train...")
    X_train_proj = pca.inverse_transform(pca.transform(X_train))
    train_spe = np.mean(np.square(X_train - X_train_proj), axis=1)

    print(">> Calcul eroare de reconstructie pe Test...")
    X_test_proj = pca.inverse_transform(pca.transform(X_test))
    test_spe = np.mean(np.square(X_test - X_test_proj), axis=1)

    # 4. Calibrare prag decizional
    threshold = np.percentile(train_spe, 99.0)
    print(f">> Prag decizional T (percentila 99 train): {threshold:.6f}")

    # 5. Clasificare pe setul de test (FARA point-adjust)
    y_pred = (test_spe > threshold).astype(int)

    # 6. Calcul metrici
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    fnr = fn / (fn + tp)  # False Negative Rate (atacuri ratate)
    fpr = fp / (fp + tn)  # False Positive Rate (alarme false)

    print("\n" + "=" * 60)
    print(">> REZULTATE BASELINE PCA (FARA POINT-ADJUST)")
    print("=" * 60)
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print(f"FNR (Atacuri ratate): {fnr*100:.2f}%")
    print(f"FPR (Alarme false):   {fpr*100:.2f}%")
    print("\nMatrice de confuzie:")
    print(f"TN: {tn:7d} | FP: {fp:7d}")
    print(f"FN: {fn:7d} | TP: {tp:7d}")
    print("=" * 60)

    return f1, prec, rec, threshold

if __name__ == "__main__":
    run_pca_baseline()