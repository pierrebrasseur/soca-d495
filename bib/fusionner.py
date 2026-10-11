"""Fusionne les .bib des séances et modules en bib/generale.bib (lancé par Quarto avant chaque rendu)."""
import re
from pathlib import Path

BIB = Path(__file__).parent
ENTREE = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,.*?\n\}", re.S)

entrees = {}
for fichier in sorted(BIB.glob("*.bib")):
    if fichier.name == "generale.bib":
        continue
    for m in ENTREE.finditer(fichier.read_text(encoding="utf-8")):
        cle, bloc = m.group(2), m.group(0)
        # À clé égale, on garde la notice la plus complète
        if cle not in entrees or bloc.count("=") > entrees[cle].count("="):
            entrees[cle] = bloc

sortie = "\n\n".join(entrees[cle] for cle in sorted(entrees)) + "\n"
cible = BIB / "generale.bib"
if not cible.exists() or cible.read_text(encoding="utf-8") != sortie:
    cible.write_text(sortie, encoding="utf-8")
