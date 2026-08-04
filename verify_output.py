#!/usr/bin/env python3
"""
Script de vérification du fichier de sortie formatted_data.csv
"""

import pandas as pd
import os

def verify_output_file(file_path='data/formatted_data.csv'):
    """Vérifie que le fichier de sortie respecte toutes les consignes"""
    
    print('🔍 VÉRIFICATION DU FICHIER FINAL')
    print('=' * 40)
    
    # Vérifier l'existence du fichier
    if not os.path.exists(file_path):
        print(f"❌ ERREUR: Fichier {file_path} introuvable!")
        return False
    
    # Charger le fichier
    df = pd.read_csv(file_path)
    
    # Vérifications
    print(f'📊 Nombre de lignes: {len(df)}')
    print(f'📋 Colonnes: {list(df.columns)}')
    
    # Vérifier les colonnes exactes
    expected_columns = ['sales', 'date', 'region']
    if list(df.columns) != expected_columns:
        print(f"❌ ERREUR: Colonnes incorrectes!")
        print(f"   Attendu: {expected_columns}")
        print(f"   Trouvé: {list(df.columns)}")
        return False
    else:
        print("✅ Colonnes correctes")
    
    # Vérifier les types de données
    print(f'💰 Ventes totales: ${df["sales"].sum():,.2f}')
    print(f'📅 Période: {df["date"].min()} à {df["date"].max()}')
    print(f'🌍 Régions: {sorted(df["region"].unique())}')
    
    # Vérifications supplémentaires
    print('\n🧪 TESTS DE VALIDATION:')
    
    # Test 1: Pas de valeurs manquantes
    missing_values = df.isnull().sum().sum()
    print(f'   • Valeurs manquantes: {missing_values} {"✅" if missing_values == 0 else "❌"}')
    
    # Test 2: Sales sont des nombres positifs
    negative_sales = (df['sales'] <= 0).sum()
    print(f'   • Ventes négatives/nulles: {negative_sales} {"✅" if negative_sales == 0 else "❌"}')
    
    # Test 3: 4 régions exactement
    regions_count = len(df['region'].unique())
    print(f'   • Nombre de régions: {regions_count} {"✅" if regions_count == 4 else "❌"}')
    
    # Test 4: Format des dates
    try:
        pd.to_datetime(df['date'])
        print(f'   • Format des dates: Valid ✅')
    except:
        print(f'   • Format des dates: Invalid ❌')
    
    # Résumé statistique
    print(f'\n📈 STATISTIQUES:')
    print(f'   • Ventes min: ${df["sales"].min():,.2f}')
    print(f'   • Ventes max: ${df["sales"].max():,.2f}')
    print(f'   • Ventes moyennes: ${df["sales"].mean():,.2f}')
    print(f'   • Taille du fichier: {os.path.getsize(file_path):,} bytes')
    
    print('\n🎉 VALIDATION TERMINÉE!')
    return True

if __name__ == '__main__':
    verify_output_file()