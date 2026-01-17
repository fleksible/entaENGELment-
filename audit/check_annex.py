import os
from pathlib import Path

GOLD = ['index/', 'policies/', 'VOIDMAP.yml', 'VOIDMAP.yaml', 'spec/', 'seeds/', 'data/receipts/']
ANNEX = ['src/', 'tools/', 'tests/', 'docs/', 'ui-app/', 'Fractalsense/', 'scripts/']
NICHTRAUM = ['NICHTRAUM/', 'INBOX/']

gold_count = 0
annex_count = 0
nichtraum_count = 0
unknown_paths = []

with open('audit/all_files.txt') as f:
    for line in f:
        path = line.strip()
        if path.startswith('./'):
            path = path[2:]
        
        is_gold = any(path.startswith(g.rstrip('/')) for g in GOLD)
        is_annex = any(path.startswith(a.rstrip('/')) for a in ANNEX)
        is_nichtraum = any(path.startswith(n.rstrip('/')) for n in NICHTRAUM)
        
        if is_gold:
            gold_count += 1
        elif is_annex:
            annex_count += 1
        elif is_nichtraum:
            nichtraum_count += 1
        else:
            # Check for root config files (typically ANNEX)
            if path.startswith('.') or '/' not in path:
                annex_count += 1  # Root config files
            else:
                unknown_paths.append(path)

print(f"GOLD files: {gold_count}")
print(f"ANNEX files: {annex_count}")
print(f"NICHTRAUM files: {nichtraum_count}")
print(f"UNKNOWN files: {len(unknown_paths)}")
if unknown_paths:
    print("\n⚠️  UNKNOWN paths:")
    for p in unknown_paths[:20]:
        print(f"  - {p}")
    if len(unknown_paths) > 20:
        print(f"  ... and {len(unknown_paths) - 20} more")
