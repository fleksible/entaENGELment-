"""Reference classifier for finite evidence features, NOT a Lean result."""
ALLOWED = frozenset({'propext', 'Classical.choice', 'Quot.sound'})
KINDS = {'RUN_FAILED':'NO_VERDICT','HOLD_DECL_MISSING':'NO_VERDICT',
         'HOLD_DECL_DUPLICATE':'NO_VERDICT','OPEN_OBLIGATION':'PROOF-VOID',
         'HOLD_TRUST_BOUNDARY':'PROOF-DEPENDENCY','FORMAL_CLOSED':'FORMAL-PROOF'}
def evidence_gate(run_ok, evidence_integrity=True, parse_known=True, full_axiom_list=True):
    if not run_ok: return 'RUN_FAILED'
    if not (evidence_integrity and parse_known and full_axiom_list):return 'HOLD_INVALID_EVIDENCE'
    return 'PASS'
def classify(run_ok: bool, decl_count: int, axioms: list[str], *, evidence_integrity=True, parse_known=True, full_axiom_list=True):
    gate=evidence_gate(run_ok,evidence_integrity,parse_known,full_axiom_list)
    if gate != 'PASS':return gate
    if decl_count==0:return 'HOLD_DECL_MISSING'
    if decl_count!=1:return 'HOLD_DECL_DUPLICATE'
    if any(not isinstance(a,str) or not a for a in axioms):return 'HOLD_INVALID_EVIDENCE'
    # Exact string equality: Foo.propext is NOT propext.
    if 'sorryAx' in axioms:return 'OPEN_OBLIGATION'
    if any(a not in ALLOWED for a in axioms):return 'HOLD_TRUST_BOUNDARY'
    return 'FORMAL_CLOSED'
def card_valid(status, visible):
    if status not in KINDS or not isinstance(visible,dict):return False
    ceiling='NONE' if status in ('RUN_FAILED','HOLD_DECL_MISSING','HOLD_DECL_DUPLICATE') else 'FORMAL'
    return (visible.get('status')==status and visible.get('kind')==KINDS[status]
            and visible.get('claim_ceiling')==ceiling
            and visible.get('semantic_reentry')=='SEPARATE_UNREVIEWED'
            and visible.get('prose_review_state')=='UNVERIFIED_PROSE')
