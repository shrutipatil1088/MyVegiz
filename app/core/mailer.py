import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(
    host: str,
    port: int,
    username: str,
    password: str,
    encryption: str,
    from_name: str,
    from_email: str,
    to_email: str,
    subject: str,
    message: str,
):
    msg = MIMEMultipart()
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    server = smtplib.SMTP(host, port)

    if encryption.upper() == "TLS":
        server.starttls()

    server.login(username, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()
