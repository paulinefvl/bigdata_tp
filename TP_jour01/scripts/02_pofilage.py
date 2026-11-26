import pandas as pd

df = pd.read_csv('data/processed/commandes_ecommerce.csv')

print("=== SHAPE ===")
print(df.shape)
print("\n=== DTYPES ===")
print(df.dtypes)
print("\n=== VALEURS MANQUANTES ===")
print(df.isna().sum())
print("\n=== DOUBLONS ===")
print(df.duplicated().sum())
print("\n=== DESCRIBE ===")
print(df.describe())