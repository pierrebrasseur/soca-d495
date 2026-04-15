#!/bin/bash
# deploy.sh — publication SOCA-D495 sur pierrebrasseur.github.io
# Usage : bash deploy.sh

set -e

REPO_DIR="$HOME/soca-d495"
REMOTE="https://github.com/pierrebrasseur/soca-d495.git"
SITE_URL="https://pierrebrasseur.github.io/soca-d495"

echo "=== SOCA-D495 — Publication GitHub Pages ==="
echo ""

# 1. Vérifier que Quarto est installé
if ! command -v quarto &> /dev/null; then
  echo "❌ Quarto n'est pas installé."
  echo "   Télécharger : https://quarto.org/docs/get-started/"
  exit 1
fi
echo "✓ Quarto $(quarto --version) détecté"

# 2. Vérifier que git est installé
if ! command -v git &> /dev/null; then
  echo "❌ Git n'est pas installé."
  exit 1
fi
echo "✓ Git $(git --version | cut -d' ' -f3) détecté"

# 3. Se placer dans le dossier
if [ ! -d "$REPO_DIR" ]; then
  echo "❌ Dossier $REPO_DIR introuvable."
  echo "   Décompresser soca-d495.zip d'abord."
  exit 1
fi
cd "$REPO_DIR"
echo "✓ Dossier : $REPO_DIR"

# 4. Compiler le site Quarto
echo ""
echo "→ Compilation Quarto..."
quarto render
echo "✓ Site compilé dans docs/"

# 5. Initialiser git si nécessaire
if [ ! -d ".git" ]; then
  echo ""
  echo "→ Initialisation du dépôt git..."
  git init
  git branch -M main
  git remote add origin "$REMOTE"
  echo "✓ Dépôt initialisé"
else
  # Vérifier/corriger le remote
  CURRENT_REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
  if [ "$CURRENT_REMOTE" != "$REMOTE" ]; then
    git remote set-url origin "$REMOTE"
    echo "✓ Remote mis à jour : $REMOTE"
  else
    echo "✓ Remote existant : $REMOTE"
  fi
fi

# 6. Commit et push
echo ""
echo "→ Commit..."
git add .
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")
git commit -m "Mise à jour du cours — $TIMESTAMP" 2>/dev/null || echo "  (rien de nouveau à committer)"

echo ""
echo "→ Push vers GitHub..."
git push -u origin main

echo ""
echo "✅ Publié avec succès !"
echo "   URL : $SITE_URL"
echo ""
echo "   GitHub Pages sera actif dans 1–2 minutes."
echo "   Activer dans Settings → Pages → Branch: main / /docs"
