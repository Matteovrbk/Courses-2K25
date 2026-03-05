"""
mail.py - Envoi automatique des emails aux opérateurs
"""
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# ─── Configuration SMTP ───────────────────────────────────────────────────────
# À configurer dans les paramètres de l'application
DEFAULT_CONFIG = {
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_user": "",
    "smtp_password": "",
    "sender_name": "Voodoo Bakery",
}


def send_schedule_emails(produit: dict, details_etapes: list[dict],
                          smtp_config: dict = None) -> tuple[bool, str]:
    """
    Envoie les emails de planning aux opérateurs concernés.
    Regroupe les étapes par opérateur.
    """
    config = smtp_config or DEFAULT_CONFIG

    if not config.get("smtp_user") or not config.get("smtp_password"):
        return False, "Configuration SMTP manquante. Emails non envoyés."

    # Regrouper les étapes par opérateur
    operateurs = {}
    for etape in details_etapes:
        email = etape.get("operateur_email")
        nom = etape.get("operateur_nom") or "Opérateur"
        if not email:
            continue
        if email not in operateurs:
            operateurs[email] = {"nom": nom, "etapes": []}
        operateurs[email]["etapes"].append(etape)

    if not operateurs:
        return False, "Aucun opérateur avec email trouvé."

    errors = []
    try:
        server = smtplib.SMTP(config["smtp_host"], config["smtp_port"])
        server.starttls()
        server.login(config["smtp_user"], config["smtp_password"])

        for email, data in operateurs.items():
            msg = _build_email(
                sender_email=config["smtp_user"],
                sender_name=config.get("sender_name", "Voodoo"),
                recipient_email=email,
                recipient_nom=data["nom"],
                produit_nom=produit["nom"],
                etapes=data["etapes"]
            )
            try:
                server.send_message(msg)
            except Exception as e:
                errors.append(f"{email}: {e}")

        server.quit()
    except Exception as e:
        return False, f"Erreur de connexion SMTP : {e}"

    if errors:
        return False, "Certains emails ont échoué : " + "; ".join(errors)
    return True, f"Emails envoyés à {len(operateurs)} opérateur(s)."


def _build_email(sender_email, sender_name, recipient_email, recipient_nom,
                  produit_nom, etapes) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🥐 Planning du jour — {produit_nom}"
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = recipient_email

    # Corps HTML
    etapes_html = ""
    for e in etapes:
        debut = e["debut"].strftime("%H:%M") if isinstance(e["debut"], datetime.datetime) else e["debut"]
        fin = e["fin"].strftime("%H:%M") if isinstance(e["fin"], datetime.datetime) else e["fin"]
        machine = e.get("machine_nom") or "—"
        etapes_html += f"""
        <tr>
            <td style="padding:8px 12px;border-bottom:1px solid #f0e6d3;">{e['etape_nom']}</td>
            <td style="padding:8px 12px;border-bottom:1px solid #f0e6d3;">{machine}</td>
            <td style="padding:8px 12px;border-bottom:1px solid #f0e6d3;font-weight:600;color:#c8783a;">{debut} → {fin}</td>
        </tr>"""

    html = f"""
    <html><body style="font-family:'Georgia',serif;background:#fdf8f0;margin:0;padding:20px;">
      <div style="max-width:600px;margin:auto;background:#fff;border-radius:12px;
                  box-shadow:0 2px 16px rgba(0,0,0,0.08);overflow:hidden;">
        <div style="background:#2c1810;padding:24px 32px;">
          <h1 style="color:#f5c842;margin:0;font-size:24px;">🥐 Voodoo Bakery</h1>
          <p style="color:#d4a96a;margin:4px 0 0;">Planning de production</p>
        </div>
        <div style="padding:24px 32px;">
          <p style="color:#2c1810;">Bonjour <strong>{recipient_nom}</strong>,</p>
          <p style="color:#555;">Voici votre planning pour la production de : 
             <strong style="color:#c8783a;">{produit_nom}</strong></p>
          <table style="width:100%;border-collapse:collapse;margin-top:16px;">
            <thead>
              <tr style="background:#fdf0e0;">
                <th style="padding:10px 12px;text-align:left;color:#2c1810;">Étape</th>
                <th style="padding:10px 12px;text-align:left;color:#2c1810;">Machine</th>
                <th style="padding:10px 12px;text-align:left;color:#2c1810;">Horaire</th>
              </tr>
            </thead>
            <tbody>{etapes_html}</tbody>
          </table>
        </div>
        <div style="padding:16px 32px;background:#fdf8f0;border-top:1px solid #f0e6d3;">
          <p style="color:#999;font-size:12px;margin:0;">
            Message généré automatiquement par Voodoo® — Gestion intelligente de l'énergie
          </p>
        </div>
      </div>
    </body></html>"""

    msg.attach(MIMEText(html, "html"))
    return msg


def send_negative_price_alert(negative_prices: list[dict],
                               recipient_email: str,
                               smtp_config: dict = None) -> tuple[bool, str]:
    """Envoie une alerte si des prix négatifs sont détectés."""
    config = smtp_config or DEFAULT_CONFIG
    if not config.get("smtp_user") or not config.get("smtp_password"):
        return False, "Configuration SMTP manquante."

    rows_html = ""
    for p in negative_prices:
        h = p["timestamp"].strftime("%H:%M") if hasattr(p["timestamp"], "strftime") else str(p["timestamp"])
        rows_html += f"<tr><td style='padding:6px 12px'>{h}</td><td style='padding:6px 12px;color:#e74c3c;font-weight:bold'>{p['price_eur_mwh']:.2f} €/MWh</td></tr>"

    html = f"""<html><body style="font-family:sans-serif">
      <h2 style="color:#e74c3c">⚡ Alerte : Prix de l'électricité négatifs</h2>
      <p>Des créneaux à prix négatif ont été détectés pour demain :</p>
      <table border="1" cellpadding="4" style="border-collapse:collapse">
        <tr><th>Heure</th><th>Prix (€/MWh)</th></tr>
        {rows_html}
      </table>
      <p style="color:#555">Profitez-en pour lancer vos process énergivores !</p>
    </body></html>"""

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "⚡ Alerte prix négatifs ENTSO-E"
        msg["From"] = f"{config.get('sender_name','Voodoo')} <{config['smtp_user']}>"
        msg["To"] = recipient_email
        msg.attach(MIMEText(html, "html"))

        server = smtplib.SMTP(config["smtp_host"], config["smtp_port"])
        server.starttls()
        server.login(config["smtp_user"], config["smtp_password"])
        server.send_message(msg)
        server.quit()
        return True, "Alerte envoyée."
    except Exception as e:
        return False, str(e)
