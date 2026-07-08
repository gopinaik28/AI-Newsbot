#!/usr/bin/env python
import os
import smtplib
import sys
from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from daily_ai_news_email_digest.crew import DailyAiNewsEmailDigestCrew


def _search_news() -> str:
    from exa_py import Exa
    exa = Exa(api_key=os.getenv("EXA_API_KEY"))
    week_ago = (date.today() - timedelta(days=7)).isoformat()

    queries = [
        f"AI artificial intelligence news {date.today().year} healthcare education",
        f"AI artificial intelligence news {date.today().year} business finance manufacturing",
    ]

    articles = []
    for q in queries:
        try:
            resp = exa.search_and_contents(
                q, num_results=4, text={"max_characters": 400},
                start_published_date=week_ago,
            )
            for r in resp.results:
                snippet = (r.text or "").strip()[:400]
                pub = getattr(r, "published_date", "recent")
                articles.append(
                    f"Headline: {r.title}\n"
                    f"URL: {r.url}\n"
                    f"Date: {pub}\n"
                    f"Snippet: {snippet}"
                )
        except Exception as e:
            print(f"[Search] Query failed: {e}", file=sys.stderr, flush=True)

    print(f"[Search] Found {len(articles)} articles", file=sys.stderr, flush=True)
    return "\n\n---\n\n".join(articles) if articles else "No articles found today."


def _send_email(subject: str, html_body: str) -> None:
    sender = os.getenv("GMAIL_ADDRESS")
    password = (os.getenv("GMAIL_APP_PASSWORD") or "").replace(" ", "")
    recipients_env = os.getenv("RECIPIENT_EMAILS", "")
    recipients = [r.strip() for r in recipients_env.split(",") if r.strip()]

    if not sender or not password:
        raise RuntimeError("GMAIL_ADDRESS or GMAIL_APP_PASSWORD not set")
    if not recipients:
        raise RuntimeError("RECIPIENT_EMAILS not set")

    print(f"[Email] Sending to {recipients}", file=sys.stderr, flush=True)

    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["To"] = sender
    msg["Bcc"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipients, msg.as_string())

    print(f"[Email] Sent to {len(recipients)} recipient(s)", file=sys.stderr, flush=True)


def run():
    today_str = date.today().strftime("%B %d, %Y")

    # Step 1: search the web (plain Python — no LLM, no tool calling)
    search_results = _search_news()

    # Step 2: crew curates, writes, and generates HTML (pure reasoning, no tools)
    result = DailyAiNewsEmailDigestCrew().crew().kickoff(inputs={
        "search_results": search_results,
        "today": today_str,
    })

    # Step 3: send email (plain Python — no LLM, no tool calling)
    _send_email(f"🤖 Daily AI News Digest — {today_str}", result.raw)


def train():
    DailyAiNewsEmailDigestCrew().crew().train(
        n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs={}
    )


def replay():
    DailyAiNewsEmailDigestCrew().crew().replay(task_id=sys.argv[1])


def test():
    DailyAiNewsEmailDigestCrew().crew().test(
        n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs={}
    )
