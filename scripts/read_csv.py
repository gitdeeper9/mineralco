#!/usr/bin/env python3
"""
Read CSV files without pandas
"""

import csv
from typing import List, Dict, Any

def read_csv_file(filename: str, skip_comments: bool = True) -> List[Dict[str, Any]]:
    """
    Read CSV file and return list of dictionaries
    
    Parameters
    ----------
    filename : str
        Path to CSV file
    skip_comments : bool
        Skip lines starting with '#'
    
    Returns
    -------
    list
        List of dictionaries with column names as keys
    """
    data = []
    
    with open(filename, 'r') as f:
        # Read all lines
        lines = [line.strip() for line in f if line.strip()]
        
        # Find header (first non-comment line)
        header = None
        for i, line in enumerate(lines):
            if not line.startswith('#'):
                header = [col.strip() for col in line.split(',')]
                start_idx = i + 1
                break
        
        if not header:
            return data
        
        # Read data
        for line in lines[start_idx:]:
            if skip_comments and line.startswith('#'):
                continue
            
            values = line.split(',')
            if len(values) == len(header):
                row = {}
                for j, col in enumerate(header):
                    # Try to convert to float if possible
                    try:
                        row[col] = float(values[j].strip())
                    except ValueError:
                        row[col] = values[j].strip()
                data.append(row)
    
    return data

def filter_by_mineral(data: List[Dict], mineral_name: str) -> List[Dict]:
    """Filter data by mineral name"""
    return [row for row in data if row.get('mineral', '').strip() == mineral_name]

def extract_columns(data: List[Dict], *columns) -> List[tuple]:
    """Extract specific columns from data"""
    result = []
    for row in data:
        values = []
        for col in columns:
            if col in row:
                values.append(row[col])
            else:
                # Try to find column by partial match
                found = False
                for key in row:
                    if col in key:
                        values.append(row[key])
                        found = True
                        break
                if not found:
                    values.append(0.0)
        result.append(tuple(values))
    return result

if __name__ == "__main__":
    # Test the reader
    data = read_csv_file("data/experimental/dac/combined_dac_data.csv")
    bridgmanite = filter_by_mineral(data, "bridgmanite")
    print(f"Found {len(bridgmanite)} bridgmanite data points")
    
    if bridgmanite:
        P_V = extract_columns(bridgmanite, "P(GPa)", "V(cm³/mol)")
        print("First 3 points:")
        for i, (P, V) in enumerate(P_V[:3]):
            print(f"  {i+1}. P={P:.1f} GPa, V={V:.2f} cm³/mol")
