import pandas as pd
def clean_mieten(file_path,cleaned_file_path):
    df = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')


    df.columns = [
        'land', 'mieten_ab_2019', 'mieten_insgesamt'
    ]
    
    df['land'] = df['land'].str.encode('ISO-8859-1').str.decode('utf-8')

    
    df['mieten_ab_2019'] = pd.to_numeric(df['mieten_ab_2019'], errors='coerce').astype('float')
    df['mieten_insgesamt'] = pd.to_numeric(df['mieten_insgesamt'], errors='coerce').astype('float')

    df['land'] = df['land'].str.replace('"', '')

    df.to_csv(cleaned_file_path, index=False)
    return df

mieten_file_path = 'data/source/nettokaltmieten.csv'
mieten_cleaned_file_path = 'data/preprocessed/cleaned_mieten.csv'
cleaned_mieten_df = clean_mieten(mieten_file_path, mieten_cleaned_file_path)