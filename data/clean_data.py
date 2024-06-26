import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError
import time

def get_lat_lon_from_plz(plz, country_code='DE', retries=1, delay=5):
    geolocator = Nominatim(user_agent="your_app_name_here", timeout=10)
    for attempt in range(retries):
        try:
            location = geolocator.geocode({'postalcode': plz, 'country': country_code})
            if location:
                return location.latitude, location.longitude
        except (GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError) as e:
            print(f"Geocoding attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    return None, None

def add_lat_lon_to_df(df):
    df['latitude'] = None
    df['longitude'] = None

    for idx, row in df.iterrows():
        plz = row['postleitzahl_hausanschrift']
        lat, lon = get_lat_lon_from_plz(plz)
        df.at[idx, 'latitude'] = lat
        df.at[idx, 'longitude'] = lon

    return df



def clean_hochschulen(file_path, cleaned_file_path):
    df = pd.read_csv(file_path, delimiter=';', dtype=str)  
    
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
    df['postleitzahl_hausanschrift'] = df['postleitzahl_hausanschrift'].astype(str)

    df = add_lat_lon_to_df(df)
    df.to_csv(cleaned_file_path, index=False)
    return df

hochschulen_file_path = 'data/source/hochschulen.csv'
hochschulen_cleaned_file_path = 'data/preprocessed/cleaned_hochschulen.csv'
cleaned_hochschulen_df = clean_hochschulen(hochschulen_file_path, hochschulen_cleaned_file_path)

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

    bundesland_mapping = {
        '01': 'Schleswig-Holstein',
        '02': 'Hamburg',
        '03': 'Niedersachsen',
        '04': 'Bremen',
        '05': 'Nordrhein-Westfalen',
        '06': 'Hessen',
        '07': 'Rheinland-Pfalz',
        '08': 'Baden-Württemberg',
        '09': 'Bayern',
        '10': 'Saarland',
        '11': 'Berlin',
        '12': 'Brandenburg',
        '13': 'Mecklenburg-Vorpommern',
        '14': 'Sachsen',
        '15': 'Sachsen-Anhalt',
        '16': 'Thüringen'
    }

    def get_region_info(region_code,region_name):
        if 'kreis' in region_name.lower():
            parts = region_name.split(',')
            region_name_clean = parts[0]
            region_type = 'kreis'
        elif ',' in region_name:
            parts = region_name.split(',')
            region_name_clean = parts[0]
            region_type = parts[1].lower()
        else:
            region_name_clean = region_name
            region_type = 'bundesland'
        
        bundesland_code = region_code[:2]
        bundesland_name = bundesland_mapping.get(bundesland_code, 'Unknown')
        
        return region_type, region_name_clean, bundesland_name

    df[['region_type', 'region_name', 'bundesland']] = df.apply(lambda x: pd.Series(get_region_info(x['region_code'], x['region_name'])), axis=1)
    
    df.to_csv(cleaned_file_path, index=False)
    return df

bevoelkerung_file_path = 'data/source/bevoelkerung.csv'
bevoelkerung_cleaned_file_path = 'data/preprocessed/cleaned_bevoelkerung.csv'
cleaned_bevoelkerung_df = clean_bevoelkerung(bevoelkerung_file_path, bevoelkerung_cleaned_file_path)
