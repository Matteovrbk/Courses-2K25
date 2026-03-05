"""
Diagnostic : affiche les clés EXACTES retournées par l'API.
Lancez ce script une fois pour vérifier les noms de champs.
"""

import requests, json

BASE_URL = "http://fky-linux01.ecam.be:5000"

print("=" * 55)
print("  DIAGNOSTIC DES CLÉS DE L'API")
print("=" * 55)

# ─── Matériaux ────────────────────────────────────────────
r = requests.get(f"{BASE_URL}/api/materials")
if r.status_code == 200:
    item = r.json()['data'][0]
    print("\n📦 /api/materials  → clés d'un matériau :")
    for k, v in item.items():
        print(f"   {repr(k):30s} = {repr(v)}")
else:
    print(f"❌ /api/materials → erreur {r.status_code}")

# ─── Variantes ────────────────────────────────────────────
r = requests.get(f"{BASE_URL}/api/variantes/id/1")
if r.status_code == 200:
    item = r.json()['data']
    print("\n🔩 /api/variantes/id/1  → clés d'une variante :")
    for k, v in item.items():
        print(f"   {repr(k):30s} = {repr(v)}")
else:
    print(f"❌ /api/variantes/id/1 → erreur {r.status_code}")

print("\n" + "=" * 55)
print("  Copiez-collez ce résultat pour corriger les clés.")
print("=" * 55)
