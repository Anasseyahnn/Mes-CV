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

## Script de génération (`_scripts/generate_cv.py`)

Automatise la copie/renommage du CV de base et l'ajout de la ligne dans `CANDIDATURES.md`.

1. Déposer le CV de base (`.docx`) dans `_base/`.
2. Vérifier `_scripts/config.json` (prénom/nom).
3. Lancer :

```bash
python _scripts/generate_cv.py --base _base/CV_base.docx --poste "AI Engineer" \
  --entreprise UNICEF --categorie AI-ML-Engineering --annee 2026 \
  --lien "https://..." --statut "Envoyée"
```
