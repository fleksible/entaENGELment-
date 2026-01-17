import os
import yaml
import json
from pathlib import Path

checks = {
    'VOIDMAP_vs_Docs': {},
    'Guards_defined': {},
    'Evidence_exists': {},
    'Missing_files': []
}

# Check 1: VOIDMAP vs docs/voids/
try:
    with open('VOIDMAP.yml') as f:
        voidmap = yaml.safe_load(f)
    voids = voidmap.get('voids', [])
    void_ids = {v['id'] for v in voids if v.get('id')}
    
    # Check docs/voids/ directory
    void_docs_dir = Path('docs/voids/')
    if void_docs_dir.exists():
        void_docs = {f.replace('.md', '') for f in os.listdir(void_docs_dir) if f.startswith('VOID-')}
    else:
        void_docs = set()
        
    checks['VOIDMAP_vs_Docs'] = {
        'total_voids': len(void_ids),
        'documented': len(void_docs),
        'missing_docs': sorted(list(void_ids - void_docs)),
        'orphaned_docs': sorted(list(void_docs - void_ids))
    }
    
    # Check evidence paths
    missing_evidence = []
    for v in voids:
        evidence = v.get('evidence')
        if evidence:
            evidence_list = evidence if isinstance(evidence, list) else [evidence]
            for path in evidence_list:
                if path and not os.path.exists(path):
                    missing_evidence.append({'void': v['id'], 'path': path})
    checks['Evidence_exists'] = {
        'missing_count': len(missing_evidence),
        'missing': missing_evidence[:10]  # First 10
    }

except Exception as e:
    checks['VOIDMAP_vs_Docs'] = {'error': str(e)}

# Check 2: Guard definitions
guard_files = [
    '.claude/rules/annex.md',
    '.claude/rules/metatron.md', 
    '.claude/rules/security.md',
    'CLAUDE.md'
]
for gf in guard_files:
    checks['Guards_defined'][gf] = os.path.exists(gf)

# Output
print(json.dumps(checks, indent=2))

# Save to file
with open('audit/consistency_report.json', 'w') as f:
    json.dump(checks, f, indent=2)
