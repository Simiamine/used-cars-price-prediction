# scripts/preprocessing.py

import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_and_clean_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)

    # Colonnes à supprimer car inutiles ou redondantes
    drop_cols = [
        'url', 'city', 'city_url', 'make', 'title_status',
        'VIN', 'size', 'image_url', 'desc', 'lat', 'long'
    ]
    df = df.drop(columns=drop_cols, errors='ignore')

    # Supprimer les lignes avec des valeurs manquantes
    df = df.dropna()

    # On garde seulement les prix entre 1 000 et 40 000 pour éviter les valeurs aberrantes
    df = df[(df['price'] > 1000) & (df['price'] < 40000)]

    # Garder les années raisonnables
    df = df[df['year'] > 2000]

    # Arrondir l’odomètre aux 5000 km pour limiter les valeurs uniques
    df['odometer'] = df['odometer'] // 5000

    # Encodage des colonnes catégorielles
    categorical_cols = df.select_dtypes(include='object').columns
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))

    # Convertir year et odometer en entiers
    df['year'] = df['year'].astype(int)
    df['odometer'] = df['odometer'].astype(int)

    return df