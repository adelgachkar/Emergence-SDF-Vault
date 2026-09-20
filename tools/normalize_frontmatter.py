# -*- coding: utf-8 -*-
"""One-shot frontmatter normalizer for the Emergence-SDF-Vault.

Rules:
- created: keep existing value; else earliest git author date of the file; else file mtime.
- license: set to CC-BY-4.0 everywhere (project convention; 14/34 already had it).
- zenodo_section: derived from the folder, then normalized to the canonical vocabulary.
- status: normalize legacy values to the canonical vocabulary (documented in Note-Template):
    draft | active | canonical | canonical-reviewed | stub-restored
- title: ensure presence, derived from the filename (Title Case with dashes preserved).
- aliases / tags / other keys: untouched.

Run from anywhere:  python tools/normalize_frontmatter.py
"""
import os
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent

FOLDER_TO_SECTION = {
    "00_MOC": "Foundations",
    "01_Foundations": "Foundations",
    "02_Geometry_Lattice": "Lattice-Geometry",
    "03_Thermodynamics_Noether": "Thermodynamics",
    "04_Emergent_Physics": "Emergent-Physics",
    "05_Literature_Grounding": "Literature-Grounding",
    "99_Templates": "Templates",
}

STATUS_ALIASES = {
    "canonical": "canonical",
    "canonical-reviewed": "canonical-reviewed",
    "active": "active",
    "draft": "draft",
    "stub-restored": "stub-restored",
    "production-ready": "canonical-reviewed",
    "reviewed": "canonical-reviewed",
    "wip": "draft",
    "in-progress": "draft",
}


def git_created(path: Path) -> str | None:
    try:
        out = subprocess.run(
            ["git", "log", "--follow", "--diff-filter=A", "--format=%ad", "--date=short", "--", str(path)],
            cwd=str(ROOT), capture_output=True, text=True, timeout=15,
        )
        dates = [l.strip() for l in out.stdout.splitlines() if l.strip()]
        return min(dates) if dates else None
    except Exception:
        return None


def mtime_date(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")


def parse_fm(text: str):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.S)
    if not m:
        return None, None, text
    return m.group(1), m.span(0), text


def get_key(block: str, key: str):
    m = re.search(rf"^{key}:\s*(.*)$", block, re.M)
    return m.group(1).strip().strip('"') if m else None


def set_key(block: str, key: str, value: str, quoted: bool = False) -> str:
    v = f'"{value}"' if quoted else value
    if re.search(rf"^{key}:\s*(.*)$", block, re.M):
        return re.sub(rf"^{key}:\s*(.*)$", rf"{key}: {v}", block, flags=re.M)
    return block.rstrip("\n") + f"\n{key}: {v}\n"


changed_report = []

for md in sorted(ROOT.rglob("*.md")):
    rel = md.relative_to(ROOT).as_posix()
    if rel.startswith((".git/", ".obsidian/", ".trash/", ".freebuff/", "tools/")):
        continue
    text = md.read_text(encoding="utf-8")
    block, span, _ = parse_fm(text)

    if block is None:
        folder = rel.split("/")[0] if "/" in rel else ""
        title = Path(rel).stem
        block = f'title: "{title}"\ncreated: {git_created(md) or mtime_date(md)}\nstatus: draft\nlicense: CC-BY-4.0\nzenodo_section: {FOLDER_TO_SECTION.get(folder, "Foundations")}\n'
        new_text = f"---\n{block}---\n\n" + text
        changed_report.append((rel, ["frontmatter created from scratch"]))
        md.write_text(new_text, encoding="utf-8", newline="\n")
        continue

    notes = []

    # --- created ---
    created = get_key(block, "created")
    if not created:
        created = git_created(md) or mtime_date(md)
        block = set_key(block, "created", created)
        notes.append(f"created={created}")

    # --- license ---
    lic = get_key(block, "license")
    if lic != "CC-BY-4.0":
        block = set_key(block, "license", "CC-BY-4.0")
        notes.append(f"license={lic or '(missing)'} -> CC-BY-4.0")

    # --- zenodo_section ---
    folder = rel.split("/")[0] if "/" in rel else ""
    zs = get_key(block, "zenodo_section")
    target = FOLDER_TO_SECTION.get(folder)
    if target and zs != target:
        block = set_key(block, "zenodo_section", target)
        notes.append(f"zenodo_section={zs or '(missing)'} -> {target}")

    # --- status ---
    st = get_key(block, "status")
    st_norm = STATUS_ALIASES.get((st or "").strip().lower())
    if st and st_norm and st_norm != st:
        block = set_key(block, "status", st_norm)
        notes.append(f"status={st} -> {st_norm}")
    elif not st:
        fallback = "active" if "Paper-" not in rel else "draft"
        block = set_key(block, "status", fallback)
        notes.append(f"status=(missing) -> {fallback}")

    # --- title (only if missing) ---
    if not get_key(block, "title"):
        block = set_key(block, "title", Path(rel).stem, quoted=True)
        notes.append("title=(missing) -> filename")

    if notes:
        new_text = text[: span[0]] + "---\n" + block + "---\n" + text[span[1]:]
        md.write_text(new_text, encoding="utf-8", newline="\n")
        changed_report.append((rel, notes))

print(f"Scanned vault root: {ROOT}\n")
if not changed_report:
    print("No changes needed.")
for rel, notes in changed_report:
    print(f"{rel}")
    for n in notes:
        print(f"    - {n}")
print(f"\n{len(changed_report)} file(s) updated.")
