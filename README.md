# 🤖 AI Newsbot — Daily AI News Email Digest

> Get a beautiful AI news email delivered to your inbox every day at 9 PM — fully automatic, no effort needed.

Every evening, 5 AI agents wake up, search the web for today's biggest AI stories across 8 industries, write a clean digest, and email it to you (and your friends). You don't have to do anything.

---

## 📬 What You Get

A nicely formatted email every day with:

- ✅ Top AI news from **8 industries** — Education, Agriculture, Banking, Healthcare, Retail, Manufacturing, Transportation & more
- ✅ **Detailed summaries** — enough to fully understand each story without clicking away
- ✅ **💡 Why it matters** — one line telling you the real-world impact
- ✅ **Read more →** links to the original source
- ✅ Sent automatically every day at **9 PM IST**

---

## 🧠 How It Works

5 AI agents run one after another, each doing one job:

```
🔍 Hunter   →   finds today's AI news across 8 sectors
🧹 Analyst  →   picks only the best, most credible stories
✍️ Writer   →   writes clear, detailed summaries
🎨 Designer →   builds the HTML email layout
📤 Sender   →   delivers it to everyone's inbox via Gmail
```

---

## 🛠️ Built With

| What | Technology |
|------|-----------|
| AI Agents | [CrewAI](https://crewai.com) |
| AI Brain | Google Gemini 2.5 Flash |
| Web Search | [Exa](https://exa.ai) |
| Email | Gmail (Python built-in) |
| Auto Schedule | GitHub Actions |
| Package Manager | [uv](https://docs.astral.sh/uv/) |

---

## 🚀 Run It Yourself

### What you need before starting
- Python 3.10 or higher
- A Gmail account
- A [Gemini API key](https://aistudio.google.com/apikey) (free)
- An [Exa API key](https://dashboard.exa.ai/api-keys) (free trial)

---

### Step 1 — Get the code

```bash
git clone https://github.com/gopinaik28/AI-Newsbot.git
cd AI-Newsbot
```

### Step 2 — Install everything

```bash
pip install uv
uv sync
```

### Step 3 — Set up your API keys

Create a file called `.env` in the project folder and fill it in:

```env
GEMINI_API_KEY=your_gemini_key_here
EXA_API_KEY=your_exa_key_here
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_APP_PASSWORD=your_app_password_here
RECIPIENT_EMAILS=you@gmail.com,friend@gmail.com
```

**Where to get each key:**

| Key | Where to get it |
|-----|----------------|
| `GEMINI_API_KEY` | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) — free |
| `EXA_API_KEY` | [dashboard.exa.ai/api-keys](https://dashboard.exa.ai/api-keys) — free trial |
| `GMAIL_APP_PASSWORD` | Google Account → Security → 2-Step Verification → App Passwords → create one, copy the 16-character password |

> 💡 **RECIPIENT_EMAILS** — comma separated. Add as many friends as you want. Everyone receives it privately via BCC (no one sees each other's email).

### Step 4 — Run it

```bash
crewai run
```

Wait 5–15 minutes. The email will arrive in your inbox. ✅

---

## ☁️ Run It Automatically Every Day (Free)

GitHub Actions runs the bot for you every day at **9 PM IST** — no computer needed.

### Step 1 — Push code to GitHub
Create a new private repository on GitHub and push this code to it.

### Step 2 — Add your secrets to GitHub

Go to your repo → **Settings → Secrets and variables → Actions → New repository secret**

Add these 5 secrets (same values as your `.env` file):

| Secret Name | Value |
|-------------|-------|
| `GEMINI_API_KEY` | Your Gemini key |
| `EXA_API_KEY` | Your Exa key |
| `GMAIL_ADDRESS` | Your Gmail address |
| `GMAIL_APP_PASSWORD` | Your app password (no spaces) |
| `RECIPIENT_EMAILS` | `you@gmail.com,friend@gmail.com` |

### Step 3 — Test it

Go to: **Actions tab → Daily AI News Digest → Run workflow → Run workflow**

If it turns green ✅ — you're done! The email will now arrive every day at 9 PM IST automatically, forever.

---

## ✏️ Customization

| What to change | Where |
|----------------|-------|
| 👥 Add/remove recipients | `RECIPIENT_EMAILS` in `.env` and GitHub secret |
| 🕘 Change the time | `.github/workflows/daily_digest.yml` → `cron:` line |
| 📰 Change sectors covered | `config/tasks.yaml` → `hunt_ai_news` |
| 🎨 Change email design | `config/tasks.yaml` → `design_html_email` |

### ⏰ Cron time quick reference (all times IST)
```
"30 15 * * *"  →  9:00 PM IST  (default)
"30 12 * * *"  →  6:00 PM IST
"30 2  * * *"  →  8:00 AM IST
```

---

## 📁 Project Structure

```
├── .github/workflows/
│   └── daily_digest.yml          # Runs the bot every day at 9 PM IST
├── src/daily_ai_news_email_digest/
│   ├── config/
│   │   ├── agents.yaml           # Who each agent is and what they do
│   │   └── tasks.yaml            # What each agent is asked to do
│   ├── tools/
│   │   └── gmail_tool.py         # Sends the email via Gmail
│   ├── crew.py                   # Connects all agents together
│   └── main.py                   # Starting point
├── .env                          # Your API keys (never shared)
├── .env.example                  # Template for setting up .env
└── pyproject.toml                # Project dependencies
```

---

## ❓ FAQ

**Do I need to keep my computer on?**
No. Once deployed to GitHub Actions, everything runs in the cloud.

**Is it free?**
Yes. Gemini and Exa both have free tiers. GitHub Actions is free for public repos and has generous free minutes for private repos.

**Can I add more people later?**
Yes — just add their email to `RECIPIENT_EMAILS` (comma separated). Everyone gets it privately via BCC.

**What if the email doesn't arrive?**
Check the Actions tab on GitHub — if the job is red, click it, copy the error, and open an issue.

---

## 📄 License

MIT
