import pandas as pd
import ast

# Load the full CSV data file
data_file_path = 'C:/Users/teo08/OneDrive/Documentos/PI/Base/credits.csv'
df = pd.read_csv(data_file_path)

# Function to parse the 'cast' and 'crew' columns from string to list of dictionaries
def parse_column(json_str):
    try:
        return ast.literal_eval(json_str)
    except (ValueError, SyntaxError):
        return []

# Apply the parsing function to the 'cast' and 'crew' columns
df['cast'] = df['cast'].apply(parse_column)
df['crew'] = df['crew'].apply(parse_column)

# Normalize the 'cast' column to create a flat DataFrame
cast_df = df.explode('cast').reset_index(drop=True)
cast_normalized = pd.json_normalize(cast_df['cast'])
cast_normalized['movie_id'] = cast_df['id']

# Normalize the 'crew' column to create a flat DataFrame
crew_df = df.explode('crew').reset_index(drop=True)
crew_normalized = pd.json_normalize(crew_df['crew'])
crew_normalized['movie_id'] = crew_df['id']

# Merge the normalized cast and crew data back into the original dataframe
cast_normalized = cast_normalized.rename(columns=lambda x: f'cast_{x}' if x != 'movie_id' else x)
crew_normalized = crew_normalized.rename(columns=lambda x: f'crew_{x}' if x != 'movie_id' else x)

# Concatenate cast and crew information on 'movie_id'
merged_df = pd.concat([cast_normalized, crew_normalized], ignore_index=True)

# Drop any redundant columns if necessary and remove duplicates
merged_df = merged_df.drop_duplicates()

# Save the cleaned data to a new CSV file
merged_df.to_csv('C:/Users/teo08/OneDrive/Documentos/PI/Base/cleaned_credits.csv', index=False)

print("Data has been cleaned and saved to a single file.")
