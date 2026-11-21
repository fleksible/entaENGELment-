# Rohausgaben-Fixtures (FIXTURE_ONLY · NOT_KERNEL_VERIFIED)

Handgeschriebene Textproben für den Leser `parse_print_axioms` / `audit_raw`
in `src/core/lean_crosswalk.py`. **Keine dieser Dateien stammt aus einem
echten Lean-Lauf.** Die Zeilenformen folgen den in der Lean-Dokumentation
gezeigten Ausgaben von `#print axioms`
(`'X' depends on axioms: [a, b]` bzw. `'X' does not depend on any axioms`).
Ob die Kommandozeile zusätzlich ein Positionspräfix wie `Datei:Zeile:Spalte: `
voranstellt, ist unbelegt; der Leser akzeptiert beide Formen, alles andere
gilt als unbekanntes Format.

| Datei | Erwartung |
| --- | --- |
| `ok_all.txt` | A, B, E → `OPEN_OBLIGATION`; C → `FORMAL_CLOSED`; D → `HOLD_TRUST_BOUNDARY`; E behält das Fremdaxiom als Zusatzbefund |
| `ok_with_position_prefix.txt` | wie `ok_all.txt` |
| `missing_decl.txt` | D → `HOLD_DECL_MISSING`, übrige wie oben |
| `duplicate_decl.txt` | C → `HOLD_DECL_DUPLICATE`, übrige wie oben |
| `wrapped_line.txt` | alle → `HOLD_INVALID_EVIDENCE` (umgebrochene Liste) |
| `unexpected_decl.txt` | alle → `HOLD_INVALID_EVIDENCE` (unerwartete Deklaration) |
| `run_failed_partial.txt` | mit Exit-Code 1: alle → `RUN_FAILED`; mit Exit-Code 0: alle → `HOLD_INVALID_EVIDENCE` |
| `lookalike_axiom.txt` | C → `HOLD_TRUST_BOUNDARY` (`Foo.propext` ist nicht `propext`) |
