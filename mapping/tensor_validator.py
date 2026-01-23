"""mapping.tensor_validator

Lightweight validator for TENSOR_MAPPING.yml.

Goal: fail fast on structural issues while keeping authoring ergonomic.
"""

from __future__ import annotations

from dataclasses import dataclass

import yaml


RCC8 = {"DC", "EC", "PO", "TPP", "NTPP", "TPPi", "NTPPi", "EQ"}
STATUS = {"defined", "partial", "void"}


@dataclass
class ValidationResult:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0


def _err(errors: list[str], msg: str) -> None:
    errors.append(msg)


def validate_tensor_mapping(filepath: str) -> ValidationResult:
    """Validate the tensor mapping YAML file."""

    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(data, dict):
        return ValidationResult(errors=["Root must be a mapping/object"], warnings=[])

    meta = data.get("metadata")
    if not isinstance(meta, dict):
        _err(errors, "metadata must be an object")
    else:
        if "version" not in meta:
            _err(errors, "metadata.version missing")
        axes = meta.get("axes")
        if not isinstance(axes, dict) or not all(k in axes for k in ("x", "y", "z")):
            _err(errors, "metadata.axes must define x,y,z")

    concepts = data.get("concepts")
    if not isinstance(concepts, list) or len(concepts) == 0:
        _err(errors, "concepts must be a non-empty list")
        return ValidationResult(errors=errors, warnings=warnings)

    names = set()
    for i, c in enumerate(concepts):
        prefix = f"concepts[{i}]"
        if not isinstance(c, dict):
            _err(errors, f"{prefix} must be an object")
            continue

        name = c.get("name")
        if not isinstance(name, str) or not name.strip():
            _err(errors, f"{prefix}.name missing or empty")
            continue

        if name in names:
            _err(errors, f"Duplicate concept name: {name}")
        names.add(name)

        coords = c.get("coordinates")
        if not isinstance(coords, dict):
            _err(errors, f"{name}: coordinates missing")
        else:
            for axis in ("x", "y"):
                ax = coords.get(axis)
                if not isinstance(ax, dict):
                    _err(errors, f"{name}: coordinates.{axis} must be object")
                else:
                    if "layer" not in ax:
                        _err(errors, f"{name}: coordinates.{axis}.layer missing")
                    elif not isinstance(ax.get("layer"), int):
                        _err(errors, f"{name}: coordinates.{axis}.layer must be int")

            z = coords.get("z")
            if not isinstance(z, str) or "Helix" not in z:
                warnings.append(f"{name}: coordinates.z should describe Helix-L/R")

        theta = c.get("theta_score")
        if theta is None:
            warnings.append(f"{name}: theta_score missing")
        else:
            if not isinstance(theta, (int, float)):
                _err(errors, f"{name}: theta_score must be number")
            elif not (0.0 <= float(theta) <= 1.0):
                warnings.append(f"{name}: theta_score={theta} outside [0,1]")

        status = c.get("status")
        if status is None:
            warnings.append(f"{name}: status missing")
        elif status not in STATUS:
            _err(errors, f"{name}: status must be one of {sorted(STATUS)}")

        rels = c.get("rcc_relations", [])
        if rels is None:
            rels = []
        if not isinstance(rels, list):
            _err(errors, f"{name}: rcc_relations must be list")
        else:
            for j, r in enumerate(rels):
                if not isinstance(r, dict):
                    _err(errors, f"{name}: rcc_relations[{j}] must be object")
                    continue
                rel = r.get("relation")
                tgt = r.get("target")
                if not isinstance(tgt, str) or not tgt.strip():
                    _err(errors, f"{name}: rcc_relations[{j}].target missing")
                if rel not in RCC8:
                    _err(errors, f"{name}: rcc_relations[{j}].relation must be RCC-8 ({sorted(RCC8)})")

    # Warn about relations to unknown targets (soft, because targets may be external or later-defined)
    for c in concepts:
        name = c.get("name")
        for r in c.get("rcc_relations", []) or []:
            tgt = r.get("target")
            if isinstance(tgt, str) and tgt not in names:
                warnings.append(f"{name}: relation target '{tgt}' not in concepts list (ok if external)")

    return ValidationResult(errors=errors, warnings=warnings)
