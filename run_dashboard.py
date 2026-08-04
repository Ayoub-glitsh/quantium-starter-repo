#!/usr/bin/env python3
"""
Soul Foods Dashboard Launcher
Quick launcher script for the Quantium dashboard application
"""

import subprocess
import sys
import os
from pathlib import Path

def check_data_file():
    """Check if required data file exists"""
    data_file = Path("data/formatted_data.csv")
    if not data_file.exists():
        print("WARNING: formatted_data.csv not found!")
        print("Please run 'python process_data.py' first to generate the data file.")
        return False
    return True

def check_virtual_env():
    """Check if virtual environment is activated"""
    if sys.prefix == sys.base_prefix:
        print("WARNING: Virtual environment not detected!")
        print("Please activate your virtual environment first:")
        print("  source ../venv/bin/activate  # or source venv/bin/activate")
        return False
    return True

def main():
    """Main launcher function"""
    print("=" * 60)
    print("QUANTIUM SOUL FOODS DASHBOARD LAUNCHER")
    print("=" * 60)
    
    # Check prerequisites
    if not check_virtual_env():
        sys.exit(1)
    
    if not check_data_file():
        print("\nWould you like to process the data now? (y/n)")
        response = input().lower().strip()
        if response == 'y':
            print("\nProcessing data...")
            try:
                subprocess.run([sys.executable, "process_data.py"], check=True)
                print("Data processing completed!")
            except subprocess.CalledProcessError:
                print("ERROR: Failed to process data")
                sys.exit(1)
        else:
            print("Exiting. Please process data first.")
            sys.exit(1)
    
    print("\nStarting Soul Foods Dashboard...")
    print("Dashboard will be available at: http://127.0.0.1:8050")
    print("Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        # Launch the dashboard
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\nDashboard stopped by user")
    except Exception as e:
        print(f"ERROR: Failed to start dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()