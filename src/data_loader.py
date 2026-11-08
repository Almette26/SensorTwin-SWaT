"""
SWaT Data Ingestion & Preprocessing Pipeline
Project: SensorTwin-SWaT (IC3 - SIVA Master, UPB)
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# 7 coloane constante identificate in literatura SWaT (Ozbek et al., 2026)
CONSTANT_COLUMNS = ['P202', 'P301', 'P401', 'P404', 'P502', 'P601', 'P603']

class SWaTDataLoader:
    def __init__(self, data_dir="../data", train_split_ratio=0.75):
        self.data_dir = data_dir
        self.train_split_ratio = train_split_ratio
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.feature_columns = []
        
    def _clean_dataframe(self, df):
        # 1. Curatare spatii albe din etichetele coloanelor
        df.columns = [col.strip() for col in df.columns]
        
        # 2. Eliminare marca temporala
        if 'Timestamp' in df.columns:
            df = df.drop(columns=['Timestamp'])
            
        # 3. Conversie eticheta in binar: 0 = Normal, 1 = Attack
        label_col = [c for c in df.columns if 'normal' in c.lower() or 'attack' in c.lower() or 'label' in c.lower()]
        if label_col:
            target = label_col[0]
            df['Label'] = df[target].apply(lambda x: 1 if str(x).strip().lower() == 'attack' else 0)
            if target != 'Label':
                df = df.drop(columns=[target])
                
        # 4. Asigurare ca toate variabilele de proces sunt numerice
        process_cols = [c for c in df.columns if c != 'Label']
        for c in process_cols:
            df[c] = pd.to_numeric(df[c], errors='coerce')
            
        # 5. Tratare valori lipsa (imputare industriala: forward-fill + backward-fill)
        df[process_cols] = df[process_cols].ffill().bfill().fillna(0)
            
        # 6. Eliminare atribute invariante (fara varianta)
        df = df.drop(columns=[col for col in CONSTANT_COLUMNS if col in df.columns])
        return df

    def load_and_preprocess(self):
        normal_path = os.path.join(self.data_dir, "normal.csv")
        attack_path = os.path.join(self.data_dir, "attack.csv")
        
        print(">> Incarcare date normale...")
        df_normal = pd.read_csv(normal_path)
        df_normal = self._clean_dataframe(df_normal)
        
        print(">> Incarcare date atac...")
        df_attack = pd.read_csv(attack_path)
        df_attack = self._clean_dataframe(df_attack)
        
        self.feature_columns = [c for c in df_normal.columns if c != 'Label']
        print(f">> Atribute de proces retinute: {len(self.feature_columns)} (eliminate 7 constante)")
        
        # Split temporal strict pe datele normale
        n_normal = len(df_normal)
        n_train = int(n_normal * self.train_split_ratio)
        
        df_train_normal = df_normal.iloc[:n_train]
        df_test_normal = df_normal.iloc[n_train:]
        
        print(f">> Split normal: {len(df_train_normal)} eșantioane Train | {len(df_test_normal)} eșantioane Test")
        
        # Construire set de test mixt (normal ramas + atacuri)
        df_test = pd.concat([df_test_normal, df_attack], ignore_index=True)
        
        # Scalare MinMax fittata exclusiv pe setul de Train
        X_train = self.scaler.fit_transform(df_train_normal[self.feature_columns].values)
        y_train = np.zeros(len(X_train), dtype=int)
        
        X_test = self.scaler.transform(df_test[self.feature_columns].values)
        y_test = df_test['Label'].values
        
        print(f">> Dimensiuni finale: Train={X_train.shape}, Test={X_test.shape}")
        print(f">> Rata de atac in Test: {np.sum(y_test)} atacuri din {len(y_test)} puncte ({np.mean(y_test)*100:.2f}%)")
        
        return X_train, y_train, X_test, y_test, self.feature_columns

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir, "data")
    
    loader = SWaTDataLoader(data_dir=dataset_path, train_split_ratio=0.75)
    X_train, y_train, X_test, y_test, features = loader.load_and_preprocess()