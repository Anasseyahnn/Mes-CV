#!/usr/bin/env python3
"""Met à jour le statut d'une candidature déjà loggée dans CANDIDATURES.md.

Usage:
    python mark_entretien.py --fichier Data-Science/Anasse_Yahanan_Data-Scientist_Yeshi-Group_2026.docx \
        --statut "Entretien programmé"

Statuts recommandés : Envoyée · Entretien programmé · Entretien réalisé · Refusée · Offre reçue
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = ROOT / "CANDIDATURES.md"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fichier", required=True, help="Chemin du CV (colonne 'Chemin CV') identifiant la ligne"
    )
    parser.add_argument("--statut", required=True, help="Nouveau statut à appliquer")
    args = parser.parse_args()

    if not LOG_PATH.exists():
        sys.exit(f"Log introuvable: {LOG_PATH}")

    lines = LOG_PATH.read_text(encoding="utf-8").splitlines()
    updated = False
    new_lines = []
    for line in lines:
        if line.strip().startswith("|") and args.fichier in line:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) == 7:
                cells[6] = args.statut
                line = "| " + " | ".join(cells) + " |"
                updated = True
        new_lines.append(line)

    if not updated:
        sys.exit(f"Aucune ligne trouvée pour: {args.fichier}")

    LOG_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print(f"Statut mis à jour -> {args.statut}")


if __name__ == "__main__":
    main()
