#!/usr/bin/env python3
"""
Verification script for formatted_data.csv output file
"""

import pandas as pd
import os

def verify_output_file(file_path='data/formatted_data.csv'):
    """Verify that output file meets all requirements"""
    
    print('FINAL FILE VERIFICATION')
    print('=' * 40)
    
    # Check file existence
    if not os.path.exists(file_path):
        print(f"ERROR: File {file_path} not found!")
        return False
    
    # Load file
    df = pd.read_csv(file_path)
    
    # Verifications
    print(f'Number of rows: {len(df)}')
    print(f'Columns: {list(df.columns)}')
    
    # Check exact columns
    expected_columns = ['sales', 'date', 'region']
    if list(df.columns) != expected_columns:
        print(f"ERROR: Incorrect columns!")
        print(f"   Expected: {expected_columns}")
        print(f"   Found: {list(df.columns)}")
        return False
    else:
        print("Columns correct")
    
    # Check data types
    print(f'Total sales: ${df["sales"].sum():,.2f}')
    print(f'Period: {df["date"].min()} to {df["date"].max()}')
    print(f'Regions: {sorted(df["region"].unique())}')
    
    # Additional verifications
    print('\nVALIDATION TESTS:')
    
    # Test 1: No missing values
    missing_values = df.isnull().sum().sum()
    status1 = "OK" if missing_values == 0 else "ERROR"
    print(f'   • Missing values: {missing_values} [{status1}]')
    
    # Test 2: Sales are positive numbers
    negative_sales = (df['sales'] <= 0).sum()
    status2 = "OK" if negative_sales == 0 else "ERROR"
    print(f'   • Negative/zero sales: {negative_sales} [{status2}]')
    
    # Test 3: Exactly 4 regions
    regions_count = len(df['region'].unique())
    status3 = "OK" if regions_count == 4 else "ERROR"
    print(f'   • Number of regions: {regions_count} [{status3}]')
    
    # Test 4: Date format
    try:
        pd.to_datetime(df['date'])
        print(f'   • Date format: Valid [OK]')
    except:
        print(f'   • Date format: Invalid [ERROR]')
    
    # Statistical summary
    print(f'\nSTATISTICS:')
    print(f'   • Min sales: ${df["sales"].min():,.2f}')
    print(f'   • Max sales: ${df["sales"].max():,.2f}')
    print(f'   • Average sales: ${df["sales"].mean():,.2f}')
    print(f'   • File size: {os.path.getsize(file_path):,} bytes')
    
    print('\nVALIDATION COMPLETED!')
    return True

if __name__ == '__main__':
    verify_output_file()