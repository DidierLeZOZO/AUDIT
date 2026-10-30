"""Écriture sûre dans Excel : un texte issu d'un PDF ne doit jamais être interprété
comme une formule (injection de formule via =, +, -, @)."""

_DECLENCHEURS = ("=", "+", "-", "@", "\t", "\r")


def neutraliser(valeur):
    if isinstance(valeur, str) and valeur.startswith(_DECLENCHEURS):
        return "'" + valeur
    return valeur


def ecrire_cellule_openpyxl(cellule, valeur):
    cellule.value = neutraliser(valeur)
