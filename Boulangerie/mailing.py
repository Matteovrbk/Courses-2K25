from email.message import EmailMessage
import smtplib
def send_operator_email(destinataire, nom_operateur, liste_taches):
    sender = "boulangerie@ecam.be"
    recipient = destinataire
    message = f"slt {nom_operateur} tu dois faire {liste_taches} "
    pwd = "cacamdp"



    email = EmailMessage()
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = "Commande"
    email.set_content(message)

    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(sender, pwd)
    smtp.send_message(email)
    smtp.quit()