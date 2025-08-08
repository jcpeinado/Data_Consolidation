import pandas as pd
from pathlib import Path

# Folder Path
user_input = r"H:\CACLA - Caledon ON\Product and Technical"
folder_path = Path(user_input)

# Main Explorer: collect relevant data
file_data = [{
    'file_name': f.stem,
    'file_path': str(f.parent),
    'parent_folder': f.parent.name,
    'file_type': f.suffix.lower().replace(".", "")
} for f in folder_path.rglob('*') if f.is_file()]

# Convert to DataFrame
df = pd.DataFrame(file_data)

# Create one-hot encoding for file_type
dummies = pd.get_dummies(df['file_type'])

# Merge dummies with main DataFrame
df_encoded = pd.concat([df[['parent_folder', 'file_name', 'file_path']], dummies], axis=1)

# Group by parent_folder and file_name
df_grouped = df_encoded.groupby(['parent_folder', 'file_name']).agg({
    'file_path': 'first',
    **{col: 'max' for col in dummies.columns}
}).reset_index()

# Convert boolean to int (0/1)
df_grouped[dummies.columns] = df_grouped[dummies.columns].astype(int)

# Show & Export result
#print(df_grouped.head())
df_grouped.to_csv('file_explorer_classified.csv', index= True)