from pathlib import Path

from registre import OUTILS, rechercher

RACINE = Path(__file__).resolve().parent.parent


def test_fichiers_existent_et_urls_uniques():
    assert all((RACINE / o.fichier).exists() for o in OUTILS)
    assert len({o.url_path for o in OUTILS}) == len(OUTILS)


def test_recherche():
    assert rechercher("odicee")[0].url_path == "suivi_cee"
    assert rechercher("") == OUTILS and rechercher("zzzz") == []
