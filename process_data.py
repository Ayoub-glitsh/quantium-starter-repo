#!/usr/bin/env python3
"""
Quantium Data Engineering Task 2: Data Processing
Soul Foods - Pink Morsel Sales Data Processing

This script processes daily sales data by:
1. Merging 3 CSV files
2. Filtering for "pink morsel" product only
3. Calculating sales (quantity * price)
4. Exporting final columns: sales, date, region
"""

import pandas as pd
import glob
import os
from pathlib import Path

def clean_price(price_str):
    """
    Clean price column by removing $ symbol and converting to float
    
    Args:
        price_str: String containing price (e.g. '$3.00')
    
    Returns:
        float: Cleaned price
    """
    if isinstance(price_str, str):
        # Remove $ symbol and convert to float
        return float(price_str.replace('$', ''))
    return float(price_str)

def load_and_merge_csv_files(data_dir='data'):
    """
    Load and merge all daily_sales_data_*.csv files
    
    Args:
        data_dir: Directory containing CSV files
    
    Returns:
        pandas.DataFrame: Merged DataFrame
    """
    # Build path to CSV files
    csv_pattern = os.path.join(data_dir, 'daily_sales_data_*.csv')
    csv_files = glob.glob(csv_pattern)
    
    if not csv_files:
        raise FileNotFoundError(f"No files found with pattern: {csv_pattern}")
    
    print(f"Files found: {len(csv_files)}")
    for file in sorted(csv_files):
        print(f"   - {file}")
    
    # Load and merge all files
    dataframes = []
    for file in sorted(csv_files):
        df = pd.read_csv(file)
        print(f"   {os.path.basename(file)}: {len(df)} rows")
        dataframes.append(df)
    
    # Merge all DataFrames
    merged_df = pd.concat(dataframes, ignore_index=True)
    print(f"Merge completed: {len(merged_df)} total rows")
    
    return merged_df

def process_sales_data(df):
    """
    Process data according to requirements:
    1. Filter for "pink morsel" only
    2. Clean prices and calculate sales
    3. Select final columns
    
    Args:
        df: Raw merged DataFrame
    
    Returns:
        pandas.DataFrame: Processed DataFrame
    """
    print("\nProcessing data...")
    
    # Step 1: Show initial structure
    print(f"Initial data: {len(df)} rows, {len(df.columns)} columns")
    print(f"   Columns: {list(df.columns)}")
    print(f"   Unique products: {df['product'].unique().tolist()}")
    
    # Step 2: Filter for "pink morsel" product (case insensitive)
    df_filtered = df[df['product'].str.lower() == 'pink morsel'].copy()
    print(f"After 'pink morsel' filtering: {len(df_filtered)} rows")
    
    if len(df_filtered) == 0:
        raise ValueError("No data found for 'pink morsel' product")
    
    # Step 3: Clean prices and calculate sales
    print("Cleaning prices and calculating sales...")
    
    # Clean price column (remove $ and convert to float)
    df_filtered['price_clean'] = df_filtered['price'].apply(clean_price)
    
    # Calculate sales (quantity * price)
    df_filtered['sales'] = df_filtered['quantity'] * df_filtered['price_clean']
    
    print(f"   Price example before: {df_filtered['price'].iloc[0]}")
    print(f"   Price example after: {df_filtered['price_clean'].iloc[0]}")
    print(f"   Sales example: {df_filtered['sales'].iloc[0]}")
    
    # Step 4: Select only required columns
    final_columns = ['sales', 'date', 'region']
    df_final = df_filtered[final_columns].copy()
    
    print(f"Final columns selected: {final_columns}")
    print(f"Final data: {len(df_final)} rows, {len(df_final.columns)} columns")
    
    return df_final

def save_processed_data(df, output_file='data/formatted_data.csv'):
    """
    Save processed DataFrame to CSV
    
    Args:
        df: Processed DataFrame
        output_file: Output path
    """
    print(f"\nSaving to: {output_file}")
    
    # Create directory if needed
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save
    df.to_csv(output_file, index=False)
    
    # Verification
    file_size = os.path.getsize(output_file)
    print(f"File saved: {output_file}")
    print(f"File size: {file_size} bytes")
    print(f"Rows exported: {len(df)}")

def display_summary(df):
    """
    Display summary of processed data
    
    Args:
        df: Final DataFrame
    """
    print("\nPROCESSED DATA SUMMARY")
    print("=" * 50)
    print(f"Total number of rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(f"Period covered: {df['date'].min()} to {df['date'].max()}")
    print(f"Regions: {sorted(df['region'].unique().tolist())}")
    print(f"Total sales: ${df['sales'].sum():,.2f}")
    print(f"Average sales per row: ${df['sales'].mean():.2f}")
    print(f"Sales min/max: ${df['sales'].min():.2f} / ${df['sales'].max():.2f}")
    
    print("\nFirst rows preview:")
    print(df.head())
    
    print("\nSales by region:")
    sales_by_region = df.groupby('region')['sales'].sum().sort_values(ascending=False)
    for region, sales in sales_by_region.items():
        print(f"   {region.capitalize()}: ${sales:,.2f}")

def main():
    """
    Main function for data processing script
    """
    print("QUANTIUM DATA PROCESSING - TASK 2")
    print("=" * 50)
    print("Client: Soul Foods")
    print("Product: Pink Morsel Sales Data")
    print("=" * 50)
    
    try:
        # Step 1: Load and merge CSV files
        df_raw = load_and_merge_csv_files()
        
        # Step 2: Process data
        df_processed = process_sales_data(df_raw)
        
        # Step 3: Save
        save_processed_data(df_processed)
        
        # Step 4: Display summary
        display_summary(df_processed)
        
        print("\nPROCESSING COMPLETED SUCCESSFULLY!")
        print("Output file: data/formatted_data.csv")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        print("Check that CSV files are present in 'data/' folder")
        raise

if __name__ == "__main__":
    main()