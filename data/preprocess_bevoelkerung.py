import pandas as pd

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