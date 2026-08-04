# Task 2: Data Processing - Soul Foods

## 📋 Objectif
Traiter les données de ventes quotidiennes de Soul Foods pour le produit "Pink Morsel" selon les consignes Quantium.

## 🚀 Exécution

### Prérequis
```bash
# Activer l'environnement virtuel
source ../venv/bin/activate  # ou source venv/bin/activate depuis la racine
```

### Traitement des données
```bash
# Exécuter le script principal
python process_data.py

# Vérifier le résultat
python verify_output.py
```

### Vérification manuelle
```bash
# Afficher les premières lignes du fichier final
head -10 data/formatted_data.csv

# Compter le nombre de lignes
wc -l data/formatted_data.csv
```

## 📊 Résultats

- **Fichiers d'entrée**: 3 CSV (41,160 lignes totales)
- **Fichier de sortie**: `data/formatted_data.csv`
- **Données traitées**: 5,880 lignes (produit "Pink Morsel" uniquement)
- **Période couverte**: 2018-02-06 à 2022-02-14
- **Régions**: East, North, South, West
- **Ventes totales**: $10,645,583.00

## 🔧 Structure du traitement

1. **Fusion** des 3 fichiers CSV
2. **Filtrage** pour "pink morsel" (insensible à la casse)
3. **Nettoyage** des prix (suppression du symbole $)
4. **Calcul** des ventes (quantity × price)
5. **Sélection** des colonnes: `sales`, `date`, `region`
6. **Export** vers `formatted_data.csv`

## ✅ Validation

Le script `verify_output.py` vérifie:
- Colonnes correctes
- Absence de valeurs manquantes
- Ventes positives
- 4 régions exactement
- Format des dates valide

## 📁 Fichiers créés

- `process_data.py` - Script principal de traitement
- `verify_output.py` - Script de vérification
- `data/formatted_data.csv` - Données traitées finales
- `TASK2_README.md` - Cette documentation