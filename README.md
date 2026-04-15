# SOCA-D495 — Théorie du travail social

Site de cours Quarto (format book) pour le cours SOCA-D495, Master en sciences du travail, Université libre de Bruxelles.

## Structure du projet

```
soca-d495/
├── _quarto.yml        # Configuration du book
├── custom.scss        # Styles personnalisés
├── index.qmd          # Page d'accueil
├── seance-1.qmd       # Séance 1 — Introduction et paradigmes
├── seance-2.qmd       # Séance 2 — Émergence historique
├── seance-3.qmd       # Séance 3 — Professionnalisation (1920–1960)
├── seance-4.qmd       # Séance 4 — Contrôle social (1970–2000)
├── seance-5.qmd       # Séance 5 — Désaffiliation (1980–2010)
├── seance-6.qmd       # Séance 6 — Genre et intersectionnalité
├── seance-7.qmd       # Séance 7 — Managérialisation et NPM
├── evaluation.qmd     # Modalités d'évaluation
├── references.qmd     # Bibliographie générale
└── docs/              # Dossier de sortie HTML (généré par Quarto)
```

## Prérequis

- [Quarto](https://quarto.org/docs/get-started/) ≥ 1.4

## Utilisation locale

```bash
# Cloner le dépôt
git clone https://github.com/brasseurph/soca-d495.git
cd soca-d495

# Prévisualiser le site en local
quarto preview

# Compiler le site
quarto render
```

Le site compilé se trouve dans le dossier `docs/`.

## Déploiement sur GitHub Pages

### 1. Créer le dépôt GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/brasseurph/soca-d495.git
git push -u origin main
```

### 2. Activer GitHub Pages

Dans les paramètres du dépôt GitHub :
- Aller dans **Settings → Pages**
- Source : **Deploy from a branch**
- Branch : `main` / dossier : `/docs`
- Cliquer sur **Save**

### 3. Mettre à jour le site

```bash
quarto render
git add docs/
git commit -m "Mise à jour du cours"
git push
```

Le site sera accessible à l'adresse : `https://brasseurph.github.io/soca-d495`

## Modifier le contenu

Chaque séance est un fichier `.qmd` (Quarto Markdown). La syntaxe est du Markdown standard avec quelques extensions Quarto :

```markdown
# Titre de section

::: {.callout-note}
**Titre de l'encadré**
Contenu de l'encadré.
:::

::: {.objectifs}
- Objectif 1
- Objectif 2
:::
```

Pour ajouter une séance, créer un fichier `seance-8.qmd` et l'ajouter dans `_quarto.yml` sous `chapters`.

## Contact

Pierre Brasseur — pierre.brasseur@ulb.be  
METICES / STRIGES — Université libre de Bruxelles
