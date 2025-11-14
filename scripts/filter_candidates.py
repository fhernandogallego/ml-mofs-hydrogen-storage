
import pandas as pd

# Cargar el archivo Excel (ajusta la ruta según ubicación local)
file_path = 'data/structuralparameters-vs-capacities-h2.dat'  # También puede ser .xlsx si usas el Excel original

# Leer los datos (usa sep apropiado si es .dat o usa pd.read_excel si es .xlsx)
df = pd.read_csv(file_path, sep='\s+', engine='python')  # Ajusta separador según formato real

# Mostrar las primeras filas
print("Dataset loaded:")
print(df.head())

# Definir funciones de filtrado para cada conjunto de targets

def filter_target_1(df):
    return df[
        (df['ugc'] >= 5.5) &
        (df['uvc'] >= 0.040) &
        (df['density'] >= 0.3) & (df['density'] <= 3.0) &
        (df['porosity'] >= 0.3) & (df['porosity'] <= 0.9) &
        (df['Ri'] >= 5) & (df['Ri'] <= 15) &
        (df['ssa'] >= 4000) & (df['ssa'] <= 6000) &
        (df['specific'] >= 1.0) & (df['specific'] <= 2.0)
    ]

def filter_target_2(df):
    return df[
        (df['ugc'] >= 5.5) &
        (df['uvc'] >= 0.020)
    ]

def filter_target_3(df):
    return df[
        (df['ugc'] >= 0.5) &
        (df['uvc'] >= 0.020)
    ]

# Aplicar filtros
filtered_1 = filter_target_1(df)
filtered_2 = filter_target_2(df)
filtered_3 = filter_target_3(df)

# Guardar resultados
filtered_1.to_csv('outputs/filtered_target1.csv', index=False)
filtered_2.to_csv('outputs/filtered_target2.csv', index=False)
filtered_3.to_csv('outputs/filtered_target3.csv', index=False)

print("Filtrados y guardados:")
print(f"Target 1: {len(filtered_1)} entries")
print(f"Target 2: {len(filtered_2)} entries")
print(f"Target 3: {len(filtered_3)} entries")
