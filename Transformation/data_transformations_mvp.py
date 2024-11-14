import pandas as pd
import ast

# Load the uploaded files
movies_dataset_path = 'C:/Users/teo08/OneDrive/Documentos/PI/Base/movies_dataset.csv'

# Load the movies dataset
movies_df = pd.read_csv(movies_dataset_path, low_memory=False)

# Transformations according to the requirements, guided by the dictionary of data

# 1. Desanidar los campos anidados: belongs_to_collection, genres, production_companies, production_countries, spoken_languages
def flatten_field(data, key):
    try:
        data_list = ast.literal_eval(data)
        if isinstance(data_list, list):
            return ', '.join([item[key] for item in data_list if key in item])
        elif isinstance(data_list, dict):
            return data_list.get(key, '')
        return ''
    except (ValueError, SyntaxError):
        return ''

# Desanidar 'belongs_to_collection' (diccionario con la información de la colección)
movies_df['belongs_to_collection'] = movies_df['belongs_to_collection'].apply(lambda x: flatten_field(x, 'name'))

# Desanidar 'genres' (lista de géneros asociados)
movies_df['genres'] = movies_df['genres'].apply(lambda x: flatten_field(x, 'name'))

# Desanidar 'production_companies' (lista de compañías de producción)
movies_df['production_companies'] = movies_df['production_companies'].apply(lambda x: flatten_field(x, 'name'))

# Desanidar 'production_countries' (lista de países de producción)
movies_df['production_countries'] = movies_df['production_countries'].apply(lambda x: flatten_field(x, 'name'))

# Desanidar 'spoken_languages' (lista de idiomas hablados)
movies_df['spoken_languages'] = movies_df['spoken_languages'].apply(lambda x: flatten_field(x, 'name'))

# 2. Rellenar valores nulos de los campos 'revenue', 'budget' con 0
movies_df['revenue'] = pd.to_numeric(movies_df['revenue'], errors='coerce').fillna(0)
movies_df['budget'] = pd.to_numeric(movies_df['budget'], errors='coerce').fillna(0)

# 3. Eliminar valores nulos del campo 'release_date'
movies_df.dropna(subset=['release_date'], inplace=True)

# 4. Formatear la fecha y crear la columna 'release_year'
movies_df['release_date'] = pd.to_datetime(movies_df['release_date'], errors='coerce').dt.strftime('%Y-%m-%d')
movies_df['release_year'] = pd.to_datetime(movies_df['release_date'], errors='coerce').dt.year

# 5. Crear la columna 'return' con el retorno de inversión
movies_df['return'] = movies_df.apply(lambda x: x['revenue'] / x['budget'] if x['budget'] > 0 else 0, axis=1)

# 6. Eliminar las columnas que no serán utilizadas
columns_to_drop = ['video', 'imdb_id', 'adult', 'original_title', 'poster_path', 'homepage']
movies_df.drop(columns=columns_to_drop, inplace=True)

# Guardar el DataFrame transformado en un archivo CSV
movies_df.to_csv('C:/Users/teo08/OneDrive/Documentos/PI/Transformation/movies_dataset_transformed.csv', index=False)

# Mostrar las primeras filas del DataFrame para verificar los cambios
print(movies_df.head())
