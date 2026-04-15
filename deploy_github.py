#!/usr/bin/env python3
"""
deploy_github.py — Publication SOCA-D495 sur pierrebrasseur.github.io

Prérequis :
  pip install PyGithub gitpython

Usage :
  python deploy_github.py --token VOTRE_TOKEN_GITHUB
  python deploy_github.py --token VOTRE_TOKEN_GITHUB --create-repo

Le token GitHub doit avoir les droits : repo (lecture/écriture)
Créer un token sur : https://github.com/settings/tokens/new
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────────────

GITHUB_USER   = "pierrebrasseur"
REPO_NAME     = "soca-d495"
REPO_DESC     = "SOCA-D495 — Théorie du travail social · ULB · Pierre Brasseur"
BRANCH        = "main"
LOCAL_DIR     = Path.home() / "soca-d495"
SITE_URL      = f"https://{GITHUB_USER}.github.io/{REPO_NAME}"

# ── Helpers ───────────────────────────────────────────────────────────────────

def run(cmd, cwd=None, check=True):
    """Exécute une commande shell et affiche la sortie."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd,
        capture_output=True, text=True
    )
    if result.stdout.strip():
        print(f"  {result.stdout.strip()}")
    if result.returncode != 0 and check:
        print(f"  ❌ Erreur : {result.stderr.strip()}")
        sys.exit(1)
    return result

def check_tool(name, install_hint):
    result = subprocess.run(f"which {name}", shell=True, capture_output=True)
    if result.returncode != 0:
        print(f"❌ {name} introuvable. {install_hint}")
        sys.exit(1)

# ── Étapes ────────────────────────────────────────────────────────────────────

def step_check_env():
    print("1. Vérification de l'environnement")
    check_tool("quarto", "Installer depuis https://quarto.org/docs/get-started/")
    check_tool("git", "Installer git depuis https://git-scm.com/")
    if not LOCAL_DIR.exists():
        print(f"❌ Dossier {LOCAL_DIR} introuvable.")
        print("   Décompressez soca-d495.zip dans votre répertoire home.")
        sys.exit(1)
    print(f"   ✓ Quarto, git et dossier {LOCAL_DIR} OK")


def step_quarto_render():
    print("\n2. Compilation Quarto")
    run("quarto render", cwd=LOCAL_DIR)
    docs = LOCAL_DIR / "docs"
    if not docs.exists():
        print("   ❌ Le dossier docs/ n'a pas été créé. Vérifiez _quarto.yml.")
        sys.exit(1)
    print("   ✓ Site compilé dans docs/")


def step_create_repo(token):
    """Crée le dépôt GitHub via l'API si il n'existe pas encore."""
    try:
        from github import Github, GithubException
    except ImportError:
        print("   ❌ PyGithub manquant. Installer avec : pip install PyGithub")
        sys.exit(1)

    print(f"\n3. Création du dépôt GitHub : {GITHUB_USER}/{REPO_NAME}")
    g = Github(token)
    user = g.get_user()
    try:
        repo = user.get_repo(REPO_NAME)
        print(f"   ✓ Dépôt existant : {repo.html_url}")
    except GithubException:
        repo = user.create_repo(
            name=REPO_NAME,
            description=REPO_DESC,
            private=False,
            auto_init=False,
        )
        print(f"   ✓ Dépôt créé : {repo.html_url}")
    return repo


def step_activate_pages(token, repo):
    """Active GitHub Pages sur branch main / /docs via l'API."""
    try:
        from github import GithubException
    except ImportError:
        return
    print("\n4. Activation de GitHub Pages")
    try:
        # L'API Pages nécessite une requête PUT non couverte par PyGithub < 2.x
        import requests
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/pages"
        payload = {"source": {"branch": BRANCH, "path": "/docs"}}
        r = requests.put(url, json=payload, headers=headers)
        if r.status_code in (200, 201, 204):
            print(f"   ✓ GitHub Pages activé → {SITE_URL}")
        elif r.status_code == 409:
            print(f"   ✓ GitHub Pages déjà actif → {SITE_URL}")
        else:
            print(f"   ⚠ Réponse API : {r.status_code} — activez manuellement dans Settings → Pages")
    except Exception as e:
        print(f"   ⚠ Activation automatique impossible ({e})")
        print("     Activer manuellement : Settings → Pages → Branch: main / /docs")


def step_git_push(token):
    print("\n5. Git — commit et push")
    remote_url = f"https://{token}@github.com/{GITHUB_USER}/{REPO_NAME}.git"

    # Init si nécessaire
    git_dir = LOCAL_DIR / ".git"
    if not git_dir.exists():
        run("git init", cwd=LOCAL_DIR)
        run(f"git branch -M {BRANCH}", cwd=LOCAL_DIR)
        run(f"git remote add origin {remote_url}", cwd=LOCAL_DIR)
        print("   ✓ Dépôt git initialisé")
    else:
        # Mettre à jour le remote avec le token
        run(f"git remote set-url origin {remote_url}", cwd=LOCAL_DIR)

    # Config git minimale
    run('git config user.email "pierre.brasseur@ulb.be"', cwd=LOCAL_DIR)
    run('git config user.name "Pierre Brasseur"', cwd=LOCAL_DIR)

    run("git add .", cwd=LOCAL_DIR)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    commit_result = run(
        f'git commit -m "Mise à jour du cours — {timestamp}"',
        cwd=LOCAL_DIR, check=False
    )
    if "nothing to commit" in (commit_result.stdout + commit_result.stderr):
        print("   ✓ Rien de nouveau à committer")
    else:
        print("   ✓ Commit créé")

    run(f"git push -u origin {BRANCH}", cwd=LOCAL_DIR)
    print("   ✓ Push réussi")


def step_summary():
    print(f"""
╔══════════════════════════════════════════════════════╗
║  ✅  Publication réussie                              ║
║                                                      ║
║  URL : {SITE_URL:<44}║
║                                                      ║
║  GitHub Pages sera en ligne dans 1 à 2 minutes.     ║
╚══════════════════════════════════════════════════════╝
""")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Déploie SOCA-D495 sur GitHub Pages")
    parser.add_argument("--token", required=True,
                        help="Token GitHub (droits repo). "
                             "Créer sur github.com/settings/tokens/new")
    parser.add_argument("--create-repo", action="store_true",
                        help="Crée le dépôt GitHub s'il n'existe pas")
    parser.add_argument("--skip-render", action="store_true",
                        help="Passe l'étape quarto render (si déjà compilé)")
    args = parser.parse_args()

    print("══════════════════════════════════════════════════════")
    print("  SOCA-D495 — Déploiement GitHub Pages")
    print(f"  {GITHUB_USER}/{REPO_NAME} → {SITE_URL}")
    print("══════════════════════════════════════════════════════\n")

    step_check_env()

    if not args.skip_render:
        step_quarto_render()
    else:
        print("\n2. Compilation Quarto — ignorée (--skip-render)")

    repo = None
    if args.create_repo:
        repo = step_create_repo(args.token)
    else:
        print(f"\n3. Dépôt GitHub — utilisation de {GITHUB_USER}/{REPO_NAME}")
        print("   (utiliser --create-repo pour créer automatiquement)")

    step_git_push(args.token)

    if repo:
        step_activate_pages(args.token, repo)

    step_summary()


if __name__ == "__main__":
    main()
