"""
Utilitaires pour accéder aux champs de l'API de façon robuste,
indépendamment de l'encodage exact des accents (é, è, ê, etc.).
"""

import unicodedata


def _normaliser(s: str) -> str:
    """Supprime les accents et met en minuscule pour la comparaison."""
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii').lower()


# Table de correspondance : nom "lisible" → clés candidates dans l'ordre de priorité
_ALIAS = {
    'Matériau':         ['Matériau', 'Materiau', 'materiau', 'Mat\u00e9riau', 'Matã©riau'],
    'Catégorie':        ['Catégorie', 'Categorie', 'categorie', 'Cat\u00e9gorie'],
    'Variante':         ['Variante', 'variante'],
    'Unité':            ['Unité', 'Unite', 'unite', 'Unit\u00e9'],
    'Prix base €':      ['Prix base €', 'Prix base', 'prix_base', 'Prix base \u20ac'],
    'Prix actuel €':    ['Prix actuel €', 'Prix actuel', 'prix_actuel', 'Prix actuel \u20ac'],
    'Variation prix %': ['Variation prix %', 'Variation prix', 'variation_prix'],
    'id_materiau':      ['id_materiau', 'id_Materiau'],
    'id_variant':       ['id_variant', 'id_variante'],
}


def get(d: dict, cle: str):
    """
    Récupère la valeur associée à une clé dans un dictionnaire renvoyé par l'API,
    en gérant automatiquement les différences d'encodage des accents.

    Exemple :
        nom = get(variante, 'Matériau')   # fonctionne même si l'API écrit 'Materiau'
    """
    # 1. Essai direct
    if cle in d:
        return d[cle]

    # 2. Essai via la table d'alias
    for alias in _ALIAS.get(cle, []):
        if alias in d:
            return d[alias]

    # 3. Comparaison normalisée (sans accents, sans casse)
    cle_norm = _normaliser(cle)
    for k, v in d.items():
        if _normaliser(k) == cle_norm:
            return v

    # 4. Recherche partielle (pour les cas "Prix base" ⊂ "Prix base €")
    for k, v in d.items():
        if cle_norm in _normaliser(k) or _normaliser(k) in cle_norm:
            return v

    raise KeyError(
        f"Champ '{cle}' introuvable.\n"
        f"Clés disponibles : {list(d.keys())}\n"
        f"→ Lancez check_api.py pour voir les noms exacts."
    )
