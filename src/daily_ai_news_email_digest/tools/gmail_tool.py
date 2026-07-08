import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class GmailSendInput(BaseModel):
    subject: str = Field(..., description="Email subject line")
    body: str = Field(..., description="Raw HTML body of the email — no markdown, no code fences")


class GmailSendTool(BaseTool):
    name: str = "gmail_send_email"
    description: str = (
        "Send an HTML email via Gmail SMTP to all configured recipients. "
        "Provide the subject line and a raw HTML string as the body."
    )
    args_schema: Type[BaseModel] = GmailSendInput

    def _run(self, subject: str, body: str) -> str:
        print(f"[GmailTool] CALLED — subject={subject!r} body_len={len(body)}", file=sys.stderr, flush=True)

        sender = os.getenv("GMAIL_ADDRESS")
        password = (os.getenv("GMAIL_APP_PASSWORD") or "").replace(" ", "")
        recipients_env = os.getenv("RECIPIENT_EMAILS", "")

        print(f"[GmailTool] sender={sender} recipients_raw={recipients_env!r}", file=sys.stderr, flush=True)

        if not sender or not password:
            raise RuntimeError("GMAIL_ADDRESS or GMAIL_APP_PASSWORD env var is missing")

        recipients = [r.strip() for r in recipients_env.split(",") if r.strip()]
        if not recipients:
            raise RuntimeError("RECIPIENT_EMAILS env var is missing or empty")

        print(f"[GmailTool] Sending to {len(recipients)} recipient(s): {recipients}", file=sys.stderr, flush=True)

        msg = MIMEMultipart("alternative")
        msg["From"] = sender
        msg["To"] = sender
        msg["Bcc"] = ", ".join(recipients)
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            failed = server.sendmail(sender, recipients, msg.as_string())

        if failed:
            raise RuntimeError(f"SMTP rejected these recipients: {failed}")

        print(f"[GmailTool] SUCCESS — sent to {len(recipients)} recipient(s)", file=sys.stderr, flush=True)
        return f"Email sent successfully to {len(recipients)} recipient(s) via BCC."
