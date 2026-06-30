# AI Newsbot — Daily AI News Email Digest

A fully automated multi-agent system that searches the web for today's top AI news across 8 industry sectors, writes a polished newsletter digest, and emails it to you every day at 9 PM IST — no manual effort required.

Built with [CrewAI](https://crewai.com), Google Gemini, Exa Search, and GitHub Actions.

---

## What It Does

Every day at 9 PM IST, 5 AI agents work in sequence:

```
Hunt → Curate → Write → Design → Send
```

| Step | Agent | Job |
|------|-------|-----|
| 1 | AI News Hunter | Searches the web for today's AI news across 8 sectors |
| 2 | AI News Analyst | Filters out noise, picks the 1-2 best stories per sector |
| 3 | Newsletter Copywriter | Writes detailed summaries with a "Why it matters" line |
| 4 | HTML Email Designer | Builds a clean, Gmail-compatible HTML email |
| 5 | Email Delivery Agent | Sends the final email via Gmail SMTP |

### Sectors Covered
Education · Agriculture · Banking & Finance · Healthcare · Retail & E-commerce · Manufacturing · Transportation · Emerging Sectors

### What the Email Looks Like
- Dark navy header with today's date
- One section per sector with a blue left-border accent
- Each story: bold headline + 4-5 sentence detailed summary + "💡 Why it matters" highlight + "Read more →" link to the source

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent framework | [CrewAI](https://crewai.com) |
| LLM | Google Gemini 2.5 Flash |
| Web search | [Exa](https://exa.ai) |
| Email delivery | Gmail SMTP (Python `smtplib`) |
| Scheduling | GitHub Actions (cron) |
| Package manager | [uv](https://docs.astral.sh/uv/) |

---

## Project Structure

```
├── .github/
│   └── workflows/
│       └── daily_digest.yml        # GitHub Actions schedule (9 PM IST daily)
├── src/daily_ai_news_email_digest/
│   ├── config/
│   │   ├── agents.yaml             # Agent roles, goals, backstories
│   │   └── tasks.yaml              # Task descriptions and pipeline
│   ├── tools/
│   │   └── gmail_tool.py           # Custom Gmail SMTP send tool
│   ├── crew.py                     # Crew wiring — agents + tasks + LLM config
│   └── main.py                     # Entry point
├── .env                            # API keys (never committed)
└── pyproject.toml                  # Dependencies
```

---

## Local Setup

### Prerequisites
- Python 3.10–3.13
- [uv](https://docs.astral.sh/uv/) — `pip install uv`

### 1. Clone the repo
```bash
git clone https://github.com/gopinaik28/AI-Newsbot.git
cd AI-Newsbot
```

### 2. Install dependencies
```bash
uv sync
```

### 3. Create your `.env` file
```bash
cp .env.example .env
```

Fill in your keys:

```env
GEMINI_API_KEY=your_gemini_api_key
EXA_API_KEY=your_exa_api_key
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password
```

| Key | Where to get it |
|-----|----------------|
| `GEMINI_API_KEY` | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |
| `EXA_API_KEY` | [dashboard.exa.ai/api-keys](https://dashboard.exa.ai/api-keys) |
| `GMAIL_ADDRESS` | Your Gmail address |
| `GMAIL_APP_PASSWORD` | Google Account → Security → 2-Step Verification → App Passwords |

### 4. Run locally
```bash
crewai run
```

The crew runs sequentially. Expect 5–15 minutes. Email arrives when complete.

---

## Automated Deployment (GitHub Actions)

The workflow in `.github/workflows/daily_digest.yml` runs every day at **9 PM IST** automatically.

### Setup steps

**1. Add secrets to your GitHub repo**

Go to: **Settings → Secrets and variables → Actions → New repository secret**

Add these 4 secrets:

| Secret name | Value |
|-------------|-------|
| `GEMINI_API_KEY` | Your Gemini API key |
| `EXA_API_KEY` | Your Exa API key |
| `GMAIL_ADDRESS` | Your Gmail address |
| `GMAIL_APP_PASSWORD` | Your app password (no spaces) |

**2. Test manually**

Go to: **Actions → Daily AI News Digest → Run workflow**

If the job completes green, the email will arrive. After that it runs on its own every day.

---

## Customization

| What to change | Where |
|----------------|-------|
| Email recipient | `config/tasks.yaml` → `send_email_newsletter` → `to:` |
| Sectors to cover | `config/tasks.yaml` → `hunt_ai_news` → description |
| Schedule time | `.github/workflows/daily_digest.yml` → `cron:` (in UTC) |
| LLM model | `crew.py` → `LLM(model=...)` on each agent |
| Email design | `config/tasks.yaml` → `design_html_email` → DESIGN SPEC |

### Cron time reference
```
"30 15 * * *"  →  9:00 PM IST (UTC+5:30)
"30 12 * * *"  →  6:00 PM IST
"30 2  * * *"  →  8:00 AM IST
```

---

## License

MIT
