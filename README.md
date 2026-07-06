# 🎯 Scout — Autonomous AI Lead Generation Agent

Scout is a background agent that hunts for freelance/hiring leads across the web,
uses an LLM to separate genuine business opportunities from noise, and serves the
results through a live dashboard — running entirely on its own, with no server
or laptop needing to stay on.

**Live dashboard:** [https://scout-ai-tawny-five.vercel.app/](#)
**Live API:** [https://scout-ai-backend-07sn.onrender.com](#)

## How it works
Hacker News API ─┐
├─► Python Scraper ─► Groq AI Classifier ─► SQLite DB
RemoteOK API ───┘ │
▼
Java Spring Boot API
│
▼
React Dashboard (live)



1. **The Scraper (Python)** polls Hacker News and RemoteOK for posts matching
   hiring/freelance keywords.
2. **The Brain (Groq / Llama 3.1)** reads each candidate post and judges whether
   it's a genuine buying-intent lead or just noise (job seekers, self-promotion,
   venting) — returning a confidence score and a one-line summary.
3. **The Database (SQLite)** stores every scanned post — not just the genuine
   ones — tagged by source. This is what powers the signal-quality tracking below.
4. **The Backend (Java / Spring Boot)** exposes a REST API over that data, with
   endpoints for genuine leads and per-source statistics.
5. **The Dashboard (React)** renders leads as a live "signal log," with a
   confidence ring per lead and a source-quality bar showing which platforms are
   actually worth scraping.
6. **GitHub Actions** runs the entire scrape → classify → commit cycle every
   6 hours automatically — no server, laptop, or manual trigger required.

---

## A real finding, not just a feature

While building this, I logged *every* AI-evaluated post (not just the ones
flagged as genuine) specifically so I could measure signal quality per source.
The result was a genuine, useful insight: **RemoteOK, despite surfacing posts
containing the word "freelance," turned out to have a near-0% genuine-lead rate**
— it's fundamentally a job board for full-time hiring, not a marketplace for
people who want to hire a freelancer for a one-off project. Hacker News,
especially informal "Ask HN" threads, produces a meaningfully higher signal rate.

The dashboard surfaces this directly, so the tool doesn't just aggregate sources —
it tells you which ones are actually worth your time.

---

## Tech stack

| Layer | Tech |
|---|---|
| Scraper | Python, `requests` |
| AI Classification | Groq (`llama-3.1-8b-instant`) |
| Database | SQLite |
| Backend API | Java 23, Spring Boot 4, Spring Data JPA |
| Frontend | React 19 (Vite), custom CSS |
| Automation | GitHub Actions (scheduled cron) |
| Deployment | Render (Docker, backend) + Vercel (frontend) |

---

## Running it locally

### 1. Database
SQLite is created automatically on first run — no setup needed.

### 2. Python agent
```bash
cd (repo root)
python -m venv venv
venv\Scripts\activate       # Windows
pip install requests groq python-dotenv
```
Create a `.env` file:
GROQ_API_KEY=your_key_here


Run a single scan cycle:
```bash
python main.py
```

### 3. Java backend
```bash
cd java-backend/backend
./gradlew bootRun
```
Runs on `http://localhost:8080`.

### 4. React dashboard
```bash
cd dashboard-react
npm install
npm run dev
```
Runs on `http://localhost:5173`, reading from `localhost:8080` by default
(configurable via `VITE_API_BASE` environment variable).

---

## Known limitations (and why)

- ~~Gemini free-tier quota (~20 requests/day)~~ — **resolved.** The pipeline
  originally used Google's Gemini API, but its free tier capped classification
  at just 20 requests/day, which the pipeline's normal match volume exceeded
  within a single scan cycle. Migrated to **Groq** (`llama-3.1-8b-instant`),
  whose free tier allows 14,400 requests/day — a ~700x increase — which fully
  removed this bottleneck.
- **SQLite is baked into the Docker image at deploy time**, not read live from
  a network database. Render's auto-deploy-on-commit means new data does
  eventually reach the live site, but a proper production version would use a
  hosted Postgres instance shared directly between the Python scraper and the
  Java backend. This would also eliminate the merge-conflict risk that comes
  with committing a binary database file alongside automated commits.
- **RemoteOK is kept in the codebase deliberately**, despite its low signal
  quality, as a demonstration of the pipeline's multi-source extensibility and
  of the signal-quality measurement feature itself.

---

## What I'd build next

- Migrate to a hosted Postgres database, removing the Docker-rebuild dependency
  and the binary-file merge-conflict risk
- Add a feedback loop: let a human mark leads as good/bad, and use that to
  refine the AI prompt over time
- Add a third source (Reddit, once developer API access is approved) now that
  the pipeline is proven to support multiple sources cleanly
Replace your .env fill-in URLs at the top with your real Vercel and Render links. Save, then:


git add README.md
git commit -m "Update README to reflect Gemini to Groq migration"
git pull origin main
git push