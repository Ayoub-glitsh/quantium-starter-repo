#!/usr/bin/env python3
"""
Quantium Data Engineering Task 2: Data Processing
Soul Foods - Pink Morsel Sales Data Processing

Ce script traite les données de ventes quotidiennes en :
1. Fusionnant les 3 fichiers CSV
2. Filtrant pour le produit "pink morsel" uniquement
3. Calculant les ventes (quantity * price)
4. Exportant les colonnes finales : sales, date, region
"""

import pandas as pd
import glob
import os
from pathlib import Path

def clean_price(price_str):
    """
    Nettoie la colonne price en supprimant le symbole $ et convertit en float
    
    Args:
        price_str: String contenant le prix (ex: '$3.00')
    
    Returns:
        float: Prix nettoyé
    """
    if isinstance(price_str, str):
        # Supprimer le symbole $ et convertir en float
        return float(price_str.replace('$', ''))
    return float(price_str)

def load_and_merge_csv_files(data_dir='data'):
    """
    Charge et fusionne tous les fichiers CSV daily_sales_data_*.csv
    
    Args:
        data_dir: Répertoire contenant les fichiers CSV
    
    Returns:
        pandas.DataFrame: DataFrame fusionné
    """
    # Construire le chemin vers les fichiers CSV
    csv_pattern = os.path.join(data_dir, 'daily_sales_data_*.csv')
    csv_files = glob.glob(csv_pattern)
    
    if not csv_files:
        raise FileNotFoundError(f"Aucun fichier trouvé avec le pattern: {csv_pattern}")
    
    print(f"📁 Fichiers trouvés : {len(csv_files)}")
    for file in sorted(csv_files):
        print(f"   - {file}")
    
    # Charger et fusionner tous les fichiers
    dataframes = []
    for file in sorted(csv_files):
        df = pd.read_csv(file)
        print(f"   ✅ {os.path.basename(file)}: {len(df)} lignes")
        dataframes.append(df)
    
    # Fusionner tous les DataFrames
    merged_df = pd.concat(dataframes, ignore_index=True)
    print(f"🔗 Fusion terminée : {len(merged_df)} lignes totales")
    
    return merged_df

def process_sales_data(df):
    """
    Traite les données selon les consignes :
    1. Filtre pour "pink morsel" uniquement
    2. Nettoie les prix et calcule les ventes
    3. Sélectionne les colonnes finales
    
    Args:
        df: DataFrame brut fusionné
    
    Returns:
        pandas.DataFrame: DataFrame traité
    """
    print("\n🔄 Traitement des données...")
    
    # Étape 1: Afficher la structure initiale
    print(f"📊 Données initiales : {len(df)} lignes, {len(df.columns)} colonnes")
    print(f"   Colonnes : {list(df.columns)}")
    print(f"   Produits uniques : {df['product'].unique().tolist()}")
    
    # Étape 2: Filtrer par produit "pink morsel" (insensible à la casse)
    df_filtered = df[df['product'].str.lower() == 'pink morsel'].copy()
    print(f"🎯 Après filtrage 'pink morsel' : {len(df_filtered)} lignes")
    
    if len(df_filtered) == 0:
        raise ValueError("Aucune donnée trouvée pour le produit 'pink morsel'")
    
    # Étape 3: Nettoyer les prix et calculer les ventes
    print("💰 Nettoyage des prix et calcul des ventes...")
    
    # Nettoyer la colonne price (supprimer $ et convertir en float)
    df_filtered['price_clean'] = df_filtered['price'].apply(clean_price)
    
    # Calculer les ventes (quantity * price)
    df_filtered['sales'] = df_filtered['quantity'] * df_filtered['price_clean']
    
    print(f"   Prix exemple avant : {df_filtered['price'].iloc[0]}")
    print(f"   Prix exemple après : {df_filtered['price_clean'].iloc[0]}")
    print(f"   Ventes exemple : {df_filtered['sales'].iloc[0]}")
    
    # Étape 4: Sélectionner uniquement les colonnes requises
    final_columns = ['sales', 'date', 'region']
    df_final = df_filtered[final_columns].copy()
    
    print(f"📋 Colonnes finales sélectionnées : {final_columns}")
    print(f"✅ Données finales : {len(df_final)} lignes, {len(df_final.columns)} colonnes")
    
    return df_final

def save_processed_data(df, output_file='data/formatted_data.csv'):
    """
    Sauvegarde le DataFrame traité en CSV
    
    Args:
        df: DataFrame traité
        output_file: Chemin de sortie
    """
    print(f"\n💾 Sauvegarde vers : {output_file}")
    
    # Créer le répertoire si nécessaire
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Sauvegarder
    df.to_csv(output_file, index=False)
    
    # Vérification
    file_size = os.path.getsize(output_file)
    print(f"✅ Fichier sauvegardé : {output_file}")
    print(f"📏 Taille du fichier : {file_size} bytes")
    print(f"📊 Lignes exportées : {len(df)}")

def display_summary(df):
    """
    Affiche un résumé des données traitées
    
    Args:
        df: DataFrame final
    """
    print("\n📈 RÉSUMÉ DES DONNÉES TRAITÉES")
    print("=" * 50)
    print(f"Nombre total de lignes : {len(df)}")
    print(f"Colonnes : {list(df.columns)}")
    print(f"Période couverte : {df['date'].min()} à {df['date'].max()}")
    print(f"Régions : {sorted(df['region'].unique().tolist())}")
    print(f"Ventes totales : ${df['sales'].sum():,.2f}")
    print(f"Ventes moyennes par ligne : ${df['sales'].mean():.2f}")
    print(f"Ventes min/max : ${df['sales'].min():.2f} / ${df['sales'].max():.2f}")
    
    print("\n📊 Aperçu des premières lignes :")
    print(df.head())
    
    print("\n🌍 Ventes par région :")
    sales_by_region = df.groupby('region')['sales'].sum().sort_values(ascending=False)
    for region, sales in sales_by_region.items():
        print(f"   {region.capitalize()}: ${sales:,.2f}")

def main():
    """
    Fonction principale du script de traitement des données
    """
    print("🚀 QUANTIUM DATA PROCESSING - TASK 2")
    print("=" * 50)
    print("Client: Soul Foods")
    print("Produit: Pink Morsel Sales Data")
    print("=" * 50)
    
    try:
        # Étape 1: Charger et fusionner les fichiers CSV
        df_raw = load_and_merge_csv_files()
        
        # Étape 2: Traiter les données
        df_processed = process_sales_data(df_raw)
        
        # Étape 3: Sauvegarder
        save_processed_data(df_processed)
        
        # Étape 4: Afficher le résumé
        display_summary(df_processed)
        
        print("\n🎉 TRAITEMENT TERMINÉ AVEC SUCCÈS!")
        print("📁 Fichier de sortie : data/formatted_data.csv")
        
    except Exception as e:
        print(f"\n❌ ERREUR : {str(e)}")
        print("🔧 Vérifiez que les fichiers CSV sont présents dans le dossier 'data/'")
        raise

if __name__ == "__main__":
    main()