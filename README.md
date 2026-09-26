# SOCA-D495 — Théories du travail social

Site de cours Quarto (format *website*) pour le cours SOCA-D495, Master en sciences du travail, Université libre de Bruxelles.

Adresse publique : https://pierrebrasseur.github.io/soca-d495

## Structure du projet

```
soca-d495/
├── _quarto.yml          # Configuration du site, navigation, barre latérale
├── index.qmd            # Accueil : parcours et modules générés à partir des séances
├── seance-1.qmd … seance-7.qmd
├── module-c5.qmd, module-c7.qmd, module-c8.qmd
├── evaluation.qmd       # Modalités d'évaluation
├── references.qmd       # Bibliographie générale
├── theme/
│   ├── light.scss       # Palette claire
│   ├── dark.scss        # Palette sombre
│   ├── rules.scss       # Styles communs (fiche de séance, objectifs, questions d'examen, accueil)
│   ├── title-block.html # En-tête « fiche » des séances
│   ├── parcours.ejs     # Gabarit du parcours et de la frise sur l'accueil
│   ├── modules.ejs      # Gabarit des cartes de modules
│   └── fonts.html       # Newsreader, Public Sans, IBM Plex Mono (Google Fonts)
└── docs/                # Site compilé, publié par GitHub Pages
```

## Métadonnées d'une séance

L'accueil lit le front matter de chaque séance et de chaque module. Modifier ces champs suffit à mettre à jour le parcours et la frise.

```yaml
title: "La mutation du contrôle social en Belgique (1970–2000)"
ref: "S4"                      # référence courte (S1…S7, C5…)
numero: "Séance 4"
bloc: "Bloc 2 · Mutations et contrôle social"
periode: "1970–2000"           # libellé affiché
debut: 1970                    # début de la bande sur la frise
fin: 2000                      # fin de la bande
description: "Une phrase pour la page d'accueil."
```

Sans `debut`/`fin`, la séance apparaît comme un fil conducteur en pointillés sur toute la frise. Pour un module, `periode` indique la séance qu'il prolonge.

Encadrés disponibles dans le texte : `::: {.objectifs}`, `::: {.question-examen}`, `::: {.callout-note}` (ou `-important`, `-warning`, `-tip`).

Pour ajouter une séance : créer `seance-8.qmd` avec ces champs, puis l'ajouter à `sidebar` dans `_quarto.yml`.

## Compiler et prévisualiser

Quarto est installé dans `~/Applications/quarto` :

```bash
~/Applications/quarto/bin/quarto preview
~/Applications/quarto/bin/quarto render
```

## Publier

GitHub Pages sert le dossier `docs/` de la branche `main`.

```bash
~/Applications/quarto/bin/quarto render
git add -A
git commit -m "Mise à jour du cours"
git push
```

## Contact

Pierre Brasseur — pierre.brasseur@ulb.be
METICES / STRIGES — Université libre de Bruxelles
