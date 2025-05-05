import os
import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, content):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SENDINBLUE_API_KEY")
    from_email = os.getenv("MAIL_FROM", "noreply@spacer.com")
    use_tls = os.getenv("SMTP_USE_TLS", "True") == "True"

    msg = MIMEText(content, "html")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            if use_tls:
                server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(from_email, [to_email], msg.as_string())
            return 200
    except Exception as e:
        print(f"Sendinblue email error: {e}")
        return None
