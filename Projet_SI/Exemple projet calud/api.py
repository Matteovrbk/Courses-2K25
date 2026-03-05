"""
api.py - Récupération du prix de l'électricité via l'API ENTSO-E
(avec fallback sur des données simulées si pas de clé API)
"""
import datetime
import math
import random
import xml.etree.ElementTree as ET

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# ─── Configuration ────────────────────────────────────────────────────────────
ENTSOE_URL = "https://web-api.tp.entsoe.eu/api"
# Zone de prix Belgique
DOMAIN_BE = "10YBE----------2"


def _simulate_prices(date: datetime.date) -> list[dict]:
    """
    Génère des prix simulés réalistes (en €/MWh) pour 24h.
    Profil typique : creux la nuit, pics matin et soir.
    """
    random.seed(date.toordinal())
    prices = []
    for hour in range(24):
        # Profil sinusoïdal avec deux pics
        base = 80
        morning_peak = 60 * math.exp(-0.5 * ((hour - 8) / 2) ** 2)
        evening_peak = 50 * math.exp(-0.5 * ((hour - 19) / 2) ** 2)
        night_dip = -30 * math.exp(-0.5 * ((hour - 3) / 2) ** 2)
        noise = random.gauss(0, 8)
        price = base + morning_peak + evening_peak + night_dip + noise
        # Parfois prix négatifs (renouvelables excédentaires)
        if hour in [2, 3, 4] and random.random() < 0.2:
            price = random.uniform(-20, -5)
        ts = datetime.datetime.combine(date, datetime.time(hour, 0))
        prices.append({"timestamp": ts, "price_eur_mwh": round(price, 2)})
    return prices


def fetch_day_ahead_prices(api_key: str | None = None,
                            date: datetime.date | None = None) -> list[dict]:
    """
    Récupère les prix day-ahead depuis ENTSO-E.
    Retourne une liste de dicts : [{timestamp: datetime, price_eur_mwh: float}, ...]
    Si l'API n'est pas disponible / pas de clé, utilise des données simulées.
    """
    if date is None:
        date = datetime.date.today() + datetime.timedelta(days=1)

    if not api_key or not REQUESTS_AVAILABLE:
        return _simulate_prices(date)

    try:
        period_start = datetime.datetime.combine(date, datetime.time(0, 0))
        period_end = period_start + datetime.timedelta(days=1)

        params = {
            "securityToken": api_key,
            "documentType": "A44",
            "in_Domain": DOMAIN_BE,
            "out_Domain": DOMAIN_BE,
            "periodStart": period_start.strftime("%Y%m%d%H00"),
            "periodEnd": period_end.strftime("%Y%m%d%H00"),
        }
        resp = requests.get(ENTSOE_URL, params=params, timeout=10)
        resp.raise_for_status()
        return _parse_entsoe_xml(resp.text, date)
    except Exception as e:
        print(f"[API] Erreur ENTSO-E, données simulées utilisées : {e}")
        return _simulate_prices(date)


def _parse_entsoe_xml(xml_text: str, date: datetime.date) -> list[dict]:
    """Parse la réponse XML ENTSO-E et extrait les prix horaires."""
    ns = {"ns": "urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:0"}
    root = ET.fromstring(xml_text)
    prices = []
    for ts_node in root.findall(".//ns:TimeSeries", ns):
        for period in ts_node.findall("ns:Period", ns):
            start_str = period.find("ns:timeInterval/ns:start", ns).text
            # Format: 2024-01-15T00:00Z
            start_dt = datetime.datetime.strptime(start_str, "%Y-%m-%dT%H:%MZ")
            resolution = period.find("ns:resolution", ns).text  # PT60M
            minutes = 60 if "60" in resolution else 30

            for i, pt in enumerate(period.findall("ns:Point", ns)):
                price = float(pt.find("ns:price.amount", ns).text)
                ts = start_dt + datetime.timedelta(minutes=i * minutes)
                prices.append({"timestamp": ts, "price_eur_mwh": round(price, 2)})

    if not prices:
        return _simulate_prices(date)
    prices.sort(key=lambda x: x["timestamp"])
    return prices


def get_negative_prices(prices: list[dict]) -> list[dict]:
    """Filtre les entrées avec prix négatif."""
    return [p for p in prices if p["price_eur_mwh"] < 0]


def compute_cost(puissance_w: float, duree_min: int,
                 prices: list[dict], start_time: datetime.datetime,
                 cout_fixe_eur: float = 0.0) -> float:
    """
    Calcule le coût énergétique d'une machine.
    puissance_w : puissance en Watts
    duree_min   : durée d'utilisation en minutes
    prices      : liste de prix horaires
    start_time  : moment de début
    cout_fixe_eur : coût fixe additionnel (ex: forfait séchoir)
    """
    if puissance_w == 0:
        return cout_fixe_eur

    end_time = start_time + datetime.timedelta(minutes=duree_min)
    total_cost = cout_fixe_eur
    puissance_kw = puissance_w / 1000.0

    for i, p in enumerate(prices):
        slot_start = p["timestamp"]
        slot_end = slot_start + datetime.timedelta(hours=1)

        # Intersection entre [start_time, end_time] et [slot_start, slot_end]
        overlap_start = max(start_time, slot_start)
        overlap_end = min(end_time, slot_end)

        if overlap_start >= overlap_end:
            continue

        overlap_hours = (overlap_end - overlap_start).total_seconds() / 3600.0
        energy_kwh = puissance_kw * overlap_hours
        # Prix en €/MWh → €/kWh = prix / 1000
        cost = energy_kwh * (p["price_eur_mwh"] / 1000.0)
        total_cost += cost

    return round(total_cost, 4)


def compute_process_cost(produit: dict, prices: list[dict],
                          start_time: datetime.datetime) -> tuple[float, list[dict]]:
    """
    Calcule le coût total d'un produit en fonction de l'heure de début.
    Retourne (coût_total, détails_étapes).
    """
    current_time = start_time
    total_cost = 0.0
    details = []

    for etape in produit["etapes"]:
        duree = etape["duree_min"]
        puissance = etape.get("puissance_w") or 0
        cout_fixe = etape.get("cout_fixe_eur") or 0.0
        machine_nom = etape.get("machine_nom") or "—"

        cost = compute_cost(puissance, duree, prices, current_time, cout_fixe)
        details.append({
            "etape_nom": etape["nom"],
            "machine_nom": machine_nom,
            "debut": current_time,
            "fin": current_time + datetime.timedelta(minutes=duree),
            "cout_eur": cost,
        })
        total_cost += cost
        current_time += datetime.timedelta(minutes=duree)

    return round(total_cost, 4), details


def find_optimal_start(produit: dict, prices: list[dict],
                        date: datetime.date) -> datetime.datetime:
    """
    Cherche l'heure de début qui minimise le coût de production sur la journée.
    Teste toutes les tranches de 15 minutes.
    """
    # Durée totale du process
    total_min = sum(e["duree_min"] for e in produit["etapes"])
    best_time = None
    best_cost = float("inf")

    start_of_day = datetime.datetime.combine(date, datetime.time(0, 0))

    # On itère par tranches de 15 min
    for offset in range(0, (24 * 60) - total_min, 15):
        candidate = start_of_day + datetime.timedelta(minutes=offset)
        cost, _ = compute_process_cost(produit, prices, candidate)
        if cost < best_cost:
            best_cost = cost
            best_time = candidate

    return best_time
