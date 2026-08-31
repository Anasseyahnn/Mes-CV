#!/usr/bin/env python3
"""Calcule le ratio CV envoyés / entretiens obtenus et met à jour BILAN.md.

Usage:
    python bilan.py
"""

import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = ROOT / "CANDIDATURES.md"
BILAN_PATH = ROOT / "BILAN.md"

OBJECTIF_ENTRETIENS = 4
STATUTS_ENTRETIEN = ("entretien programmé", "entretien réalisé")
STATUTS_BROUILLON = ("brouillon",)


def parse_rows() -> list[dict]:
    if not LOG_PATH.exists():
        sys.exit(f"Log introuvable: {LOG_PATH}")

    rows = []
    for line in LOG_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 7 or cells[0] in ("Date", "---"):
            continue
        if set(cells[0]) <= {"-"}:
            continue
        rows.append(
            {
                "date": cells[0],
                "poste": cells[1],
                "entreprise": cells[2],
                "categorie": cells[3],
                "lien": cells[4],
                "fichier": cells[5],
                "statut": cells[6],
            }
        )
    return rows


def is_brouillon(statut: str) -> bool:
    return any(s in statut.lower() for s in STATUTS_BROUILLON)


def is_entretien(statut: str) -> bool:
    return any(s in statut.lower() for s in STATUTS_ENTRETIEN)


def main() -> None:
    rows = parse_rows()
    envoyees = [r for r in rows if not is_brouillon(r["statut"])]
    entretiens = [r for r in envoyees if is_entretien(r["statut"])]

    today = date.today()
    week_ago = today - timedelta(days=7)

    def in_last_week(r: dict) -> bool:
        try:
            d = date.fromisoformat(r["date"])
        except ValueError:
            return False
        return week_ago <= d <= today

    envoyees_semaine = [r for r in envoyees if in_last_week(r)]
    entretiens_semaine = [r for r in entretiens if in_last_week(r)]

    total_envoyees = len(envoyees)
    total_entretiens = len(entretiens)
    ratio = (total_entretiens / total_envoyees * 100) if total_envoyees else 0.0
    reste = max(0, OBJECTIF_ENTRETIENS - total_entretiens)

    par_categorie: dict[str, dict[str, int]] = {}
    for r in envoyees:
        c = par_categorie.setdefault(r["categorie"], {"envoyees": 0, "entretiens": 0})
        c["envoyees"] += 1
        if is_entretien(r["statut"]):
            c["entretiens"] += 1

    lines = []
    lines.append(f"## Bilan du {today.isoformat()}")
    lines.append("")
    lines.append(f"- Objectif : {OBJECTIF_ENTRETIENS} entretiens")
    lines.append(f"- Entretiens obtenus (total) : {total_entretiens}/{OBJECTIF_ENTRETIENS} — reste {reste}")
    lines.append(f"- CV envoyés (total) : {total_envoyees}")
    lines.append(f"- Ratio entretien/candidature (total) : {ratio:.1f}%")
    lines.append(f"- Cette semaine : {len(envoyees_semaine)} CV envoyés, {len(entretiens_semaine)} entretiens")
    if par_categorie:
        lines.append("")
        lines.append("| Catégorie | CV envoyés | Entretiens | Ratio |")
        lines.append("|---|---|---|---|")
        for cat, c in sorted(par_categorie.items()):
            r = (c["entretiens"] / c["envoyees"] * 100) if c["envoyees"] else 0.0
            lines.append(f"| {cat} | {c['envoyees']} | {c['entretiens']} | {r:.0f}% |")
    lines.append("")

    report = "\n".join(lines)

    if BILAN_PATH.exists():
        existing = BILAN_PATH.read_text(encoding="utf-8")
    else:
        existing = "# Bilan hebdomadaire — CV envoyés vs entretiens obtenus\n\n"

    header, _, rest = existing.partition("\n\n")
    BILAN_PATH.write_text(header + "\n\n" + report + "\n" + rest, encoding="utf-8")

    print(report)


if __name__ == "__main__":
    main()
