import csv
import unittest
from pathlib import Path

from src.core.lean_crosswalk import ALLOWED, classify

ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "lean_crosswalk"


def rows(name):
    with (ROOT / "tables" / name).open(newline="", encoding="utf8") as f:
        return list(csv.DictReader(f))


class ContractTables(unittest.TestCase):
    def test_truth_table_exhaustive(self):
        items = rows("derivation_truth_table.csv")
        self.assertEqual(len(items), 24)
        seen = set()
        for t in items:
            ok = t["run_ok"] == "True"
            co = t["decl_count"]
            so = t["has_sorry"] == "True"
            fr = t["has_foreign"] == "True"
            self.assertNotIn((ok, co, so, fr), seen)
            seen.add((ok, co, so, fr))
            axioms = (["sorryAx"] if so else []) + (["Foo.propext"] if fr else [])
            decl = 0 if co == "0" else 1 if co == "1" else 2
            self.assertEqual(classify(ok, decl, axioms), t["expected_status"])
        self.assertEqual(len(seen), 2 * 3 * 2 * 2)

    # v0.3 test_audit_matrix_exhaustive entfernt: er prüfte nur die Tabelle gegen
    # sich selbst. Ersetzt durch test_audit_matrix_runs_against_card_validator
    # in test_lean_crosswalk_gegenfaelle.py (7x7, echter Kartenprüfer).
    def test_fail_closed(self):
        for p in [
            {"evidence_integrity": False},
            {"parse_known": False},
            {"full_axiom_list": False},
        ]:
            self.assertEqual(classify(True, 1, [], **p), "HOLD_INVALID_EVIDENCE")
        self.assertEqual(classify(False, 1, []), "RUN_FAILED")
        self.assertEqual(classify(True, 0, []), "HOLD_DECL_MISSING")
        self.assertEqual(classify(True, 2, []), "HOLD_DECL_DUPLICATE")

    def test_axiom_exact_match(self):
        for allowed in ALLOWED:
            self.assertEqual(classify(True, 1, [allowed]), "FORMAL_CLOSED")
        for foreign in [
            "Foo.propext",
            "Lean.trustCompiler",
            "Lean.ofReduceBool",
            "_native_decide.ax1",
        ]:
            self.assertEqual(classify(True, 1, [foreign]), "HOLD_TRUST_BOUNDARY")
        self.assertEqual(classify(True, 1, ["Foo.propext", "sorryAx"]), "OPEN_OBLIGATION")

    def test_card_rules(self):
        # v0.3 prüfte fünf Felder über card_valid(status, card); jetzt Karte gegen Urteil und Herkunft.
        from src.core.lean_crosswalk import STATUSES, assess, build_card, validate_card

        examples = {
            "RUN_FAILED": assess(False, 1, []),
            "HOLD_INVALID_EVIDENCE": assess(True, 1, [], parse_known=False),
            "HOLD_DECL_MISSING": assess(True, 0, []),
            "HOLD_DECL_DUPLICATE": assess(True, 2, []),
            "OPEN_OBLIGATION": assess(True, 1, ["sorryAx"]),
            "HOLD_TRUST_BOUNDARY": assess(True, 1, ["Foo.propext"]),
            "FORMAL_CLOSED": assess(True, 1, []),
        }
        self.assertEqual(set(examples), set(STATUSES))
        for verdict in examples.values():
            card = build_card(verdict, "a" * 64)
            self.assertEqual(validate_card(card, verdict, "a" * 64), ())
            for key, bad in [
                ("kind", "EPI-VOID"),
                ("claim_ceiling", "FACT"),
                ("semantic_reentry", "REVIEWED"),
                ("prose_review_state", "CERTIFIED"),
            ]:
                mutated = dict(card)
                mutated[key] = bad
                self.assertNotEqual(validate_card(mutated, verdict, "a" * 64), ())


if __name__ == "__main__":
    unittest.main()
