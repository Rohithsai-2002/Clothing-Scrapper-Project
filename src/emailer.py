import smtplib
from email.message import EmailMessage

def send_email(subject: str, body: str, smtp_config: dict):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp_config.get("from") or smtp_config.get("username")
    msg["To"] = ", ".join(smtp_config.get("to", []))
    msg.set_content(body)

    host = smtp_config.get("host")
    port = smtp_config.get("port", 587)
    username = smtp_config.get("username")
    password = smtp_config.get("password")

    with smtplib.SMTP(host, port, timeout=20) as s:
        s.starttls()
        if username and password:
            s.login(username, password)
        s.send_message(msg)
