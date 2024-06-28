import pandas as pd
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