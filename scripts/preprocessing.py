import pandas as pd

def preprocess_vehicle_data(path="../data/vehicles.csv"):
    df = pd.read_csv(path)

    # Supprimer colonnes inutiles
    cols_to_drop = [
        'url', 'region_url', 'VIN', 'lat', 'long', 'image_url',
        'description', 'id', 'region', 'county'
    ]
    df.drop(columns=cols_to_drop, inplace=True)

    # Garder uniquement les colonnes utiles
    columns_to_keep = [
        'price', 'year', 'manufacturer', 'condition', 'cylinders',
        'fuel', 'odometer', 'transmission', 'drive', 'type',
        'paint_color', 'state', 'title_status', 'posting_date'
    ]
    df = df[columns_to_keep]

    # Supprimer les lignes avec NaN
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)

    # ✅ Transformation en datetime avec prise en charge des fuseaux horaires mixtes
    df['posting_date'] = pd.to_datetime(df['posting_date'], errors='coerce', utc=True)

    # 🔎 Filtrer les lignes avec conversion échouée
    df = df[df['posting_date'].notna()]

    # Extraire des informations temporelles
    df['year_posted'] = df['posting_date'].dt.year
    df['month_posted'] = df['posting_date'].dt.month
    df['weekday_posted'] = df['posting_date'].dt.weekday

    # Filtrer les prix aberrants
    df = df[(df['price'] > 100) & (df['price'] < 250000)]
    
    # Optionnel : supprimer la colonne brute
    df.drop(columns=['posting_date'], inplace=True)

    return df