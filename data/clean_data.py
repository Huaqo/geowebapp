import pandas as pd
import numpy as np

def clean_hochschulen(file_path, cleaned_file_path):
    df = pd.read_csv(file_path, delimiter=';')

    df.columns = [
        'hochschulkurzname', 'hochschulname', 'hochschultyp', 'traegerschaft', 
        'bundesland', 'anzahl_studierende', 'gruendungsjahr', 'promotionsrecht', 
        'habilitationsrecht', 'strasse', 'postleitzahl_hausanschrift', 
        'ort_hausanschrift', 'home_page'
    ]

    df['promotionsrecht'] = df['promotionsrecht'].map({'Ja': True, 'Nein': False})
    df['habilitationsrecht'] = df['habilitationsrecht'].map({'Ja': True, 'Nein': False})

    df.dropna(subset=['hochschulkurzname', 'hochschulname', 'hochschultyp', 'traegerschaft', 'bundesland', 
                      'anzahl_studierende', 'gruendungsjahr', 'promotionsrecht', 'habilitationsrecht', 
                      'strasse', 'postleitzahl_hausanschrift', 'ort_hausanschrift', 'home_page'], how='any', inplace=True)


    df['anzahl_studierende'] = pd.to_numeric(df['anzahl_studierende'], errors='coerce').astype('Int64')
    df['gruendungsjahr'] = pd.to_numeric(df['gruendungsjahr'], errors='coerce').astype('Int64')
    df['postleitzahl_hausanschrift'] = pd.to_numeric(df['postleitzahl_hausanschrift'], errors='coerce').astype('Int64')

    df.to_csv(cleaned_file_path, index=False)
    return df

def clean_bevoelkerung(file_path,cleaned_file_path):
    df = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1', skiprows=8)

    df.columns = [
        'region_code', 'region_name', 'total_population', 'male_population', 'female_population'
    ]

    df['total_population'] = pd.to_numeric(df['total_population'], errors='coerce').astype('Int64')
    df['male_population'] = pd.to_numeric(df['male_population'], errors='coerce').astype('Int64')
    df['female_population'] = pd.to_numeric(df['female_population'], errors='coerce').astype('Int64')

    df = df.dropna(subset=['region_code', 'region_name', 'total_population', 'male_population', 'female_population'])

    df['region_name'] = df['region_name'].str.replace(' ', '')

    df.to_csv(cleaned_file_path, index=False)
    return df

hochschulen_file_path = 'data/source/hochschulen.csv'
hochschulen_cleaned_file_path = 'data/preprocessed/cleaned_hochschulen.csv'
cleaned_hochschulen_df = clean_hochschulen(hochschulen_file_path, hochschulen_cleaned_file_path)

bevoelkerung_file_path = 'data/source/bevoelkerung.csv'
bevoelkerung_cleaned_file_path = 'data/preprocessed/cleaned_bevoelkerung.csv'
cleaned_bevoelkerung_df = clean_bevoelkerung(bevoelkerung_file_path, bevoelkerung_cleaned_file_path)
