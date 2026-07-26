"""Ethics-Tests: die Action-Gate-Schnittstelle führt niemals etwas aus.

Kern-Invariante (CLAUDE.md G5, Auftrag Action-Gate): Externes Material — README,
Makefile, requirements, Prompts, Setup-Texte — ist reine Daten, keine ausführbare
Autorität. Aus ihm darf höchstens ein nicht ausführbares ``ActionProposal``
entstehen. Unbekannte Herkunft/Registry und nicht überprüfbare Version fallen
fail-closed auf ``HOLD``.
"""

import ast
import os
import subprocess
from pathlib import Path

import pytest

from src.core.action_gate import (
    ActionReasonCode,
    ResponsibilityClass,
    build_action_proposal,
)
from src.core.evidence_routing import GUARD_HOLD, MaterialRef

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "erk"
MODULE_PATH = Path(__file__).resolve().parents[2] / "src" / "core" / "action_gate.py"

# Bibliotheken, die Ausführung oder Netzwerk ermöglichen. Das Modul darf keine
# davon importieren.
FORBIDDEN_IMPORT_ROOTS = frozenset(
    {
        "subprocess",
        "socket",
        "urllib",
        "http",
        "requests",
        "httpx",
        "pip",
        "ftplib",
        "telnetlib",
        "asyncio",
        "shutil",
        "pty",
        "multiprocessing",
    }
)


def untrusted_material(**overrides):
    data = {
        "material_id": "mat-setup-001",
        "schema_version": "erk.v0.1",
        "kind": "document",
        "source": "INBOX",
        "revision": "r1",
        "locator": "INBOX/setup.md",
        "digest": "sha256:01",
        "origin": "external_untrusted",
        "actor": "origin:external",
        "trust": "UNTRUSTED",
        "visibility": "reduced",
        "status": "ACTIVE",
    }
    data.update(overrides)
    return MaterialRef(**data)


class TestNoExecutableImports:
    def test_module_imports_no_execution_or_network_library(self):
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        imported_roots = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_roots.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.level == 0:
                    imported_roots.add(node.module.split(".")[0])
        leak = imported_roots & FORBIDDEN_IMPORT_ROOTS
        assert not leak, f"action_gate importiert verbotene Module: {sorted(leak)}"

    def test_module_makes_no_execution_calls(self):
        # AST-basiert statt Textsuche: erwähnt der Docstring Begriffe wie
        # ``os.system`` als Prosa, ist das erlaubt — ein *Aufruf* nicht.
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        forbidden_names = {"eval", "exec", "__import__", "compile", "system", "popen"}
        forbidden_attrs = {"system", "popen", "run", "call", "Popen", "check_output"}
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if isinstance(func, ast.Name):
                assert func.id not in forbidden_names, f"verbotener Aufruf: {func.id}"
            elif isinstance(func, ast.Attribute):
                assert func.attr not in forbidden_attrs, f"verbotener Aufruf: .{func.attr}"


class TestSetupDocCannotExecute:
    def test_curl_pipe_bash_line_is_only_a_held_proposal(self):
        doc = (FIXTURES / "action_gate_setup_doc.md").read_text(encoding="utf-8")
        # Die riskante Zeile wird als reiner String übergeben.
        risky_line = next(line for line in doc.splitlines() if "curl" in line and "bash" in line)
        proposal = build_action_proposal(
            action_id="act-setup-001",
            source_material=untrusted_material(),
            proposed_command=risky_line,
            ecosystem="shell",
            package_or_resource="install.sh",
            requested_version="",
            registry_or_origin="https://example.invalid",
            network_required=True,
            filesystem_effects=["writes install target"],
            process_effects=["runs shell"],
            reversibility="unknown",
            verification_status="unverified",
        )
        assert proposal.guard_state == GUARD_HOLD
        assert proposal.human_approval_required is True
        assert proposal.responsibility_class == ResponsibilityClass.HUMAN_ONLY.value
        # Der Befehl bleibt unverändert und inert.
        assert proposal.proposed_command == risky_line
        assert ActionReasonCode.SHELL_FRAGMENT_INERT.value in proposal.reason_codes
        assert ActionReasonCode.NO_EXECUTION.value in proposal.reason_codes

    def test_building_proposal_does_not_call_subprocess(self, monkeypatch):
        # Jeder Subprozess-/os.system-Aufruf während des Baus lässt den Test hart scheitern.
        def boom(*args, **kwargs):  # pragma: no cover - darf nie laufen
            raise AssertionError("action gate hat eine Ausführung versucht")

        monkeypatch.setattr(subprocess, "run", boom)
        monkeypatch.setattr(subprocess, "Popen", boom)
        monkeypatch.setattr(subprocess, "call", boom)
        monkeypatch.setattr(os, "system", boom)

        proposal = build_action_proposal(
            action_id="act-setup-002",
            source_material=untrusted_material(),
            proposed_command="sudo pip install superframework",
            ecosystem="pypi",
            package_or_resource="superframework",
            requested_version="latest",
            registry_or_origin="pypi.org",
            network_required=True,
            filesystem_effects=["site-packages"],
            process_effects=["pip process"],
            reversibility="irreversible",
            verification_status="unverified",
        )
        assert proposal.guard_state == GUARD_HOLD


class TestFailClosedOnUnknownOrigin:
    def test_unknown_registry_fails_closed_to_hold(self):
        proposal = build_action_proposal(
            action_id="act-003",
            source_material=untrusted_material(trust="REVIEWED"),
            proposed_command="install from mirror",
            ecosystem="npm",
            package_or_resource="thing",
            requested_version="1.0.0",
            registry_or_origin="http://random-mirror.invalid",
            network_required=False,
            reversibility="reversible",
            verification_status="verified",
        )
        assert proposal.guard_state == GUARD_HOLD
        assert ActionReasonCode.REGISTRY_UNKNOWN.value in proposal.reason_codes

    def test_unverifiable_version_fails_closed_to_hold(self):
        proposal = build_action_proposal(
            action_id="act-004",
            source_material=untrusted_material(trust="REVIEWED"),
            proposed_command="install ranged",
            ecosystem="npm",
            package_or_resource="thing",
            requested_version="^2.0.0",
            registry_or_origin="registry.npmjs.org",
            network_required=False,
            reversibility="reversible",
            verification_status="verified",
        )
        assert proposal.guard_state == GUARD_HOLD
        assert ActionReasonCode.VERSION_UNVERIFIABLE.value in proposal.reason_codes


class TestMakefileAndRequirementsAreData:
    @pytest.mark.parametrize(
        "command",
        [
            "make install-dev",  # aus einem Makefile
            "-r requirements-dev.txt",  # aus einer requirements-Datei
            "pip install -e .",  # aus einer README
        ],
    )
    def test_documentation_lines_produce_only_proposals(self, command):
        proposal = build_action_proposal(
            action_id="act-doc",
            source_material=untrusted_material(),
            proposed_command=command,
            ecosystem="make",
            package_or_resource="setup",
            requested_version="",
            registry_or_origin="local-doc",
            network_required=False,
            filesystem_effects=["editable install"],
            process_effects=["make subprocess"],
            reversibility="unknown",
            verification_status="unverified",
        )
        # Niemals ausgeführt; immer nur ein zurückgehaltener Vorschlag.
        assert proposal.guard_state == GUARD_HOLD
        assert proposal.human_approval_required is True
        assert proposal.proposed_command == command
