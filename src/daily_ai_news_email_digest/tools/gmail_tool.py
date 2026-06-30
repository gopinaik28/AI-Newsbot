import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class GmailSendInput(BaseModel):
    to: str = Field(..., description="Recipient email address")
    subject: str = Field(..., description="Email subject line")
    body: str = Field(..., description="Raw HTML body of the email — no markdown, no code fences")


class GmailSendTool(BaseTool):
    name: str = "gmail_send_email"
    description: str = (
        "Send an HTML email via Gmail SMTP. "
        "Provide the recipient address, subject line, and a raw HTML string as the body."
    )
    args_schema: Type[BaseModel] = GmailSendInput

    def _run(self, to: str, subject: str, body: str) -> str:
        sender = os.getenv("GMAIL_ADDRESS")
        password = (os.getenv("GMAIL_APP_PASSWORD") or "").replace(" ", "")

        if not sender or not password:
            return "Error: GMAIL_ADDRESS or GMAIL_APP_PASSWORD is not set in .env"

        msg = MIMEMultipart("alternative")
        msg["From"] = sender
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, to, msg.as_string())

        return f"Email sent successfully to {to} with subject: {subject}"
