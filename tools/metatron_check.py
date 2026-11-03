#!/usr/bin/env python3
"""
Metatron-Guard: Prüft ob FOKUS deklariert ist.
Bei FOKUS-SWITCH muss Frage vorhanden sein.

Usage:
    echo "PR Body text" | python metatron_check.py
    python metatron_check.py < pr_body.txt
    python metatron_check.py --help

Exit Codes:
    0 = PASS (all checks passed)
    1 = FAIL (missing FOKUS or question after FOKUS-SWITCH)
"""

from __future__ import annotations

import argparse
import re
import sys

# Pattern für FOKUS: Marker (case-insensitive)
# Erwartet: "FOKUS: <mindestens ein Wort>"
RX_FOKUS = re.compile(r"^[ \t]*FOKUS[ \t]*:[ \t]*\S+", re.IGNORECASE | re.MULTILINE)

# GitHub's commented template examples are not visible declarations.
RX_HTML_COMMENT = re.compile(r"<!--.*?(?:-->|$)", re.DOTALL)

# Pattern für FOKUS-SWITCH: Marker (captures rest of line and following content)
# Varianten: FOKUS-SWITCH, FOKUS_SWITCH, FOKUS SWITCH; optional numbered switches.
RX_SWITCH = re.compile(r"FOKUS[-_\s]*SWITCH(?:[ \t]+\d+)?\s*:", re.IGNORECASE)

# Pattern für Frage (Zeile endet mit ?)
RX_QUESTION = re.compile(r"\?\s*$", re.MULTILINE)

# Max lines after FOKUS-SWITCH to search for question
MAX_LINES_AFTER_SWITCH = 5


def visible_text(text: str) -> str:
    # Keep line boundaries so hiding a comment cannot move a later question closer.
    return RX_HTML_COMMENT.sub(lambda match: re.sub(r"[^\n]", " ", match.group()), text)


def has_question_after_switch(text: str) -> bool:
    """
    Check if there's a question within MAX_LINES_AFTER_SWITCH lines after FOKUS-SWITCH.

    Returns:
        True if question found in the appropriate section, False otherwise.
    """
    switches = list(RX_SWITCH.finditer(text))
    for index, match in enumerate(switches):
        # A question for a later switch cannot authorize an earlier one.
        end = switches[index + 1].start() if index + 1 < len(switches) else len(text)
        section = text[match.end() : end]
        lines_after = section.split("\n")[: MAX_LINES_AFTER_SWITCH + 1]
        if not RX_QUESTION.search("\n".join(lines_after)):
            return False
    return True


def check_text(text: str) -> tuple[bool, list[str]]:
    """
    Prüft den Text auf Metatron-Guard Compliance.

    Args:
        text: Der zu prüfende Text (z.B. PR-Body)

    Returns:
        Tuple von (success, errors)
        - success: True wenn alle Checks bestanden
        - errors: Liste von Fehlermeldungen
    """
    text = visible_text(text)
    errors: list[str] = []

    # Check 1: FOKUS: muss vorhanden sein
    if not RX_FOKUS.search(text):
        errors.append("Missing required marker: `FOKUS:`")

    # Check 2: Wenn FOKUS-SWITCH vorhanden, muss Frage in den nächsten Zeilen folgen
    if RX_SWITCH.search(text) and not has_question_after_switch(text):
        errors.append(
            f"Found `FOKUS-SWITCH:` but no question (line ending with `?`) "
            f"within {MAX_LINES_AFTER_SWITCH} lines after the marker."
        )

    return (len(errors) == 0), errors


def main() -> int:
    """
    Hauptfunktion - liest von stdin und prüft.

    Returns:
        Exit Code (0 = PASS, 1 = FAIL)
    """
    parser = argparse.ArgumentParser(
        description="Metatron-Guard: Check for FOKUS markers in PR body",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    echo "FOKUS: Setup guards" | python metatron_check.py
    cat pr_body.txt | python metatron_check.py

Exit Codes:
    0 = PASS
    1 = FAIL
        """,
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed output even on success",
    )
    args = parser.parse_args()

    # Lese von stdin
    text = sys.stdin.read()

    if not text.strip():
        print("Warning: Empty input received")
        print("METATRON-GUARD: FAIL (empty input)")
        return 1

    # Prüfung durchführen
    ok, errs = check_text(text)

    if not ok:
        for e in errs:
            print(f"Error: {e}")
        print("METATRON-GUARD: FAIL")
        return 1

    if args.verbose:
        print("Checks passed:")
        print("  - FOKUS: marker found")
        if RX_SWITCH.search(visible_text(text)):
            print("  - FOKUS-SWITCH: found with question")

    print("METATRON-GUARD: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
