# Mes-CV

Archive des CV adaptés générés pour chaque candidature envoyée. Ce repo est alimenté automatiquement par une routine de recherche d'emploi qui dépose un CV `.docx` par offre postulée (potentiellement plusieurs par jour).

## Objectif

Garder une trace complète et consultable de chaque version de CV produite pour une candidature spécifique, classée par catégorie de poste, avec un log centralisé dans [`CANDIDATURES.md`](./CANDIDATURES.md).

## Convention de nommage des fichiers

```
Prénom_Nom_Intitulé-Poste_Entreprise_Année.docx
```

Règles :
- Underscores (`_`) entre les blocs, tirets (`-`) à l'intérieur d'un intitulé multi-mots
- Pas d'espaces
- Pas d'accents ni de caractères spéciaux
- Année = année de la candidature

**Exemple :** `Anasse_Yahanan_AI-Engineer_UNICEF_2026.docx`

## Structure des dossiers

Chaque CV est rangé dans le dossier correspondant à la catégorie du poste visé :

| Dossier | Catégorie |
|---|---|
| `Data-Science/` | Data Science |
| `AI-ML-Engineering/` | AI / Machine Learning Engineering |
| `LLM-Engineering/` | LLM Engineering |
| `MEAL-Suivi-Evaluation/` | MEAL / Suivi-Évaluation |
| `Charge-Etudes-Marketing/` | Chargé d'Études Marketing |
| `Autre/` | Toute autre catégorie ne rentrant pas dans les précédentes |

Chaque candidature envoyée doit être loggée dans [`CANDIDATURES.md`](./CANDIDATURES.md).

## Objectif de campagne

**4 entretiens minimum**, sur des postes à responsabilité (Lead / Head / Manager) en Data Science, IA ou Ingénierie LLM, cohérents avec le profil GitHub/portfolio.

## Script de génération (`_scripts/generate_cv.py`)

Automatise la copie/renommage du CV de base, l'adaptation du titre à l'offre, et l'ajout de la ligne dans `CANDIDATURES.md`.

1. Le CV de base (`.docx`) est dans `_base/CV_base.docx`, généré par `_scripts/build_master_cv.py` (source éditable — modifier ce script plutôt que le `.docx` directement, puis relancer `python _scripts/build_master_cv.py`).
2. Vérifier `_scripts/config.json` (prénom/nom).
3. Lancer :

```bash
python _scripts/generate_cv.py --poste "Lead Data Scientist" --entreprise UNICEF \
  --categorie AI-ML-Engineering --annee 2026 --lien "https://..." \
  --titre "Lead Data Scientist — UNICEF"
```

`--titre` adapte l'accroche du CV (2e ligne) à l'offre visée ; `--base` reste disponible pour utiliser un autre fichier de base.

## Suivi des candidatures

Statuts standardisés (colonne `Statut` de `CANDIDATURES.md`) :

`Brouillon — en attente de validation` → `Envoyée` → `Entretien programmé` → `Entretien réalisé` → `Refusée` / `Offre reçue`

Pour mettre à jour le statut d'une candidature déjà loggée :

```bash
python _scripts/mark_entretien.py --fichier "Data-Science/Anasse_Yahanan_....docx" --statut "Entretien programmé"
```

## Bilan hebdomadaire (`_scripts/bilan.py`)

Calcule le ratio CV envoyés / entretiens obtenus (total + 7 derniers jours + par catégorie) et l'ajoute en tête de `BILAN.md`.

```bash
python _scripts/bilan.py
```
