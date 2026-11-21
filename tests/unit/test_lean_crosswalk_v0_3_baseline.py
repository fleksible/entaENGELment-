import sys,unittest,csv,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"fixtures"/"lean_crosswalk"
from src.core.lean_crosswalk import classify,card_valid,ALLOWED,KINDS

def rows(name):
    with (ROOT/'tables'/name).open(newline='',encoding='utf8') as f:return list(csv.DictReader(f))
class ContractTables(unittest.TestCase):
    def test_truth_table_exhaustive(self):
        items=rows('derivation_truth_table.csv');self.assertEqual(len(items),24)
        seen=set()
        for t in items:
            ok=t['run_ok']=='True';co=t['decl_count'];so=t['has_sorry']=='True';fr=t['has_foreign']=='True'
            self.assertNotIn((ok,co,so,fr),seen);seen.add((ok,co,so,fr))
            axioms=(['sorryAx'] if so else [])+(['Foo.propext'] if fr else [])
            decl=0 if co=='0' else 1 if co=='1' else 2
            self.assertEqual(classify(ok,decl,axioms),t['expected_status'])
        self.assertEqual(len(seen),2*3*2*2)
    def test_audit_matrix_exhaustive(self):
        items=rows('audit_matrix.csv');self.assertEqual(len(items),36)
        for t in items:self.assertEqual(t['verdict'], 'PASS' if t['expected_status']==t['visible_status'] else 'REJECT')
    def test_fail_closed(self):
        for p in [{'evidence_integrity':False},{'parse_known':False},{'full_axiom_list':False}]:
            self.assertEqual(classify(True,1,[],**p),'HOLD_INVALID_EVIDENCE')
        self.assertEqual(classify(False,1,[]),'RUN_FAILED')
        self.assertEqual(classify(True,0,[]),'HOLD_DECL_MISSING')
        self.assertEqual(classify(True,2,[]),'HOLD_DECL_DUPLICATE')
    def test_axiom_exact_match(self):
        for allowed in ALLOWED:self.assertEqual(classify(True,1,[allowed]),'FORMAL_CLOSED')
        for foreign in ['Foo.propext','Lean.trustCompiler','Lean.ofReduceBool','_native_decide.ax1']:
            self.assertEqual(classify(True,1,[foreign]),'HOLD_TRUST_BOUNDARY')
        self.assertEqual(classify(True,1,['Foo.propext','sorryAx']),'OPEN_OBLIGATION')
    def test_card_rules(self):
        for s in KINDS:
            card={'status':s,'kind':KINDS[s],'claim_ceiling':'NONE' if KINDS[s]=='NO_VERDICT' else 'FORMAL',
                  'semantic_reentry':'SEPARATE_UNREVIEWED','prose_review_state':'UNVERIFIED_PROSE'}
            self.assertTrue(card_valid(s,card))
            for key,bad in [('kind','EPI-VOID'),('claim_ceiling','FACT'),('semantic_reentry','REVIEWED'),('prose_review_state','CERTIFIED')]:
                mutated=dict(card);mutated[key]=bad;self.assertFalse(card_valid(s,mutated))
if __name__=='__main__':unittest.main()
