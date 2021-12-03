
import smtplib
import ssl
from email.message import EmailMessage


class Postman:

    """Deliver email messages."""

    __smtp_server: str = None
    __sender_email: str = None
    __password: str = ""


    def __init__(self, smtp_server: str, sender_email: str, password: str = ""):
        self.__smtp_server = smtp_server
        self.__sender_email = sender_email
        self.__password = password


    def send(self, email: str, subject: str = "", text: str = "") -> None:

        msg = EmailMessage()
        msg["From"] = self.__sender_email
        msg["To"] = email
        msg["Subject"] = subject
        msg.set_content(text)

        with smtplib.SMTP_SSL(self.__smtp_server, context=ssl.create_default_context()) as server:
            server.login(self.__sender_email, self.__password)
            server.send_message(msg)
