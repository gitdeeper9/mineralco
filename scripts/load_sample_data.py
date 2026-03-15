#!/usr/bin/env python3
"""
Sample script to load MINERALCO data files
"""

import json
import csv
import os
from pathlib import Path

def load_cis_database():
    """Load CIS database"""
    db_path = Path("data/databases/cis/cis_database_v1.0.0.json")
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return None
    
    with open(db_path, 'r') as f:
        data = json.load(f)
    
    print(f"✅ Loaded CIS database v{data['metadata']['version']}")
    print(f"   {len(data['minerals'])} minerals")
    print(f"   Source: {data['metadata']['source']}")
    
    # Print first 5 minerals
    print("\nFirst 5 minerals:")
    for i, mineral in enumerate(data['minerals'][:5]):
        print(f"   {i+1}. {mineral['name']:15s} ({mineral['formula']}) - "
              f"K₀={mineral['K0']:.1f} GPa, K'={mineral['Kprime']:.2f}")
    
    return data

def load_pvt_benchmark():
    """Load P-V-T benchmark data"""
    csv_path = Path("data/experimental/dac/combined_dac_data.csv")
    if not csv_path.exists():
        print(f"❌ Benchmark not found: {csv_path}")
        return None
    
    minerals = {}
    total_points = 0
    
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # Skip empty rows
            if not row or len(row) == 0:
                continue
            # Skip comment lines
            if row[0].startswith('#'):
                continue
            # Ensure row has enough columns
            if len(row) >= 2:
                mineral = row[0].strip()
                if mineral:  # Only count non-empty mineral names
                    if mineral not in minerals:
                        minerals[mineral] = 0
                    minerals[mineral] += 1
                    total_points += 1
    
    print(f"\n✅ Loaded P-V-T benchmark data")
    print(f"   Total data points: {total_points}")
    print(f"   Minerals with data:")
    for mineral, count in sorted(minerals.items()):
        print(f"   - {mineral}: {count} points")
    
    return minerals

def load_space_groups():
    """Load space groups database"""
    sg_path = Path("data/databases/space_groups/space_groups_230.json")
    if not sg_path.exists():
        print(f"❌ Space groups not found: {sg_path}")
        return None
    
    with open(sg_path, 'r') as f:
        data = json.load(f)
    
    print(f"\n✅ Loaded space groups database")
    print(f"   {len(data['space_groups'])} space groups")
    print(f"   Crystal systems: {', '.join(data['crystal_systems'].keys())}")
    
    return data

def load_prem():
    """Load PREM reference"""
    prem_path = Path("data/reference/prem/prem_1981_updated.csv")
    if not prem_path.exists():
        print(f"❌ PREM not found: {prem_path}")
        return None
    
    data_points = 0
    with open(prem_path, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                data_points += 1
    
    print(f"\n✅ Loaded PREM reference")
    print(f"   {data_points} depth points")
    
    return data_points

def load_minerals_by_system():
    """Load minerals by system file"""
    ms_path = Path("data/databases/mineral_list/minerals_by_system.json")
    if not ms_path.exists():
        print(f"❌ Minerals by system not found: {ms_path}")
        return None
    
    with open(ms_path, 'r') as f:
        data = json.load(f)
    
    total = sum(data['statistics'].values())
    print(f"\n✅ Loaded minerals by system")
    print(f"   {total} minerals across {len(data['by_system'])} crystal systems")
    
    return data

if __name__ == "__main__":
    print("=" * 50)
    print("MINERALCO Data Files Loader")
    print("=" * 50)
    
    cis = load_cis_database()
    pvt = load_pvt_benchmark()
    sg = load_space_groups()
    prem = load_prem()
    ms = load_minerals_by_system()
    
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"✓ CIS database: {len(cis['minerals']) if cis else 0} minerals" if cis else "✗ CIS database: Not found")
    
    if pvt:
        total_pvt = sum(pvt.values())
        print(f"✓ P-V-T data: {total_pvt} points from {len(pvt)} minerals")
    else:
        print("✗ P-V-T data: Not found")
    
    print(f"✓ Space groups: {len(sg['space_groups']) if sg else 0} groups" if sg else "✗ Space groups: Not found")
    print(f"✓ PREM data: {prem} depth points" if prem else "✗ PREM data: Not found")
    
    if ms:
        total_minerals = sum(ms['statistics'].values())
        print(f"✓ Minerals by system: {total_minerals} minerals")
    else:
        print("✗ Minerals by system: Not found")
    
    print("=" * 50)
