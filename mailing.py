from email.message import EmailMessage
import smtplib


def send_operator_email(destinataire, nom_operateur, liste_taches):
    sender = "23356@ecam.be"
    recipient = destinataire
    message = f"Bonjour {nom_operateur},\n\nVoici vos tâches pour aujourd'hui :\n{liste_taches}\n\nCordialement,\nVoodoo"
    pwd = "Evame73934"

    email = EmailMessage()
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = "Commande - Planning machines"
    email.set_content(message)

    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(sender, pwd)
    smtp.send_message(email)
    smtp.quit()
