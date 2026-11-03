# 📧 AI Customer Support System

An end-to-end generative AI pipeline that automates customer support for an e-commerce company. The system monitors a Gmail inbox, classifies incoming queries, retrieves company-specific knowledge from a database, and drafts professional replies—all while maintaining strict brand guidelines and safety guardrails.

## 🚀 Features

- **Gmail Automation**: Synchronizes with Gmail via OAuth2 to read and reply to customer threads.
- **Agentic RAG**: Uses a multi-agent architecture (Classifier $\rightarrow$ Support Agent) that uses tools to query a knowledge base.
- **Structured Output**: Leverages **Pydantic AI** to ensure the LLM returns valid JSON for internal state management.
- **Safety Guardrails**: Implemented "guards" to prevent AI loops, block bulk mail, and prevent the AI from promising refunds or dates.
- **Evaluation Suite**: A "Golden Set" of 18 test cases to measure accuracy and prevent regressions during prompt tuning.
- **State Management**: Uses **Supabase (PostgreSQL)** to track conversations, event processing, and knowledge base articles.

## 🛠 Tech Stack

- **LLM**: Groq (GPT-OSS-120B for drafting, GPT-OSS-20B for triage)
- **Framework**: [Pydantic AI](https://pydantic-ai.com)
- **Database**: Supabase (PostgreSQL)
- **API**: FastAPI
- **Infrastructure**: Docker, Hostinger VPS
- **Language**: Python 3.13

## 🏗 Architecture

1. **The Poller**: A background worker that checks Gmail every 30s for unread messages.
2. **The Guards**: A rule-based filter that skips auto-replies, bulk mail, or sent messages.
3. **The Classifier**: An AI agent that determines the topic (e.g., `shipping`, `returns`) and checks if the email needs human escalation.
4. **The Support Agent**: A tool-using agent that retrieves specific sections of the knowledge base and drafts a reply following the company's "Brand and Tone" guide.
5. **The Decision Engine**: A final Python layer that validates the AI's proposal against hard business rules before sending the email.

## 📈 Evaluation Results

The system is tested against a "Golden Set" of 18 realistic customer scenarios.
- **Section Accuracy**: ~87%
- **Action Accuracy**: ~87%
The evaluation suite allows for rapid prompt iteration without manual testing.

## ⚙️ Setup

### 1. Environment Variables
Create a `.env` file based on `.env.example`:
```env
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GOOGLE_REFRESH_TOKEN=...
DATABASE_URL=...
GROQ_API_KEY=...
```

### 2. Database Setup
Run the migrations provided in the project to set up the `knowledge_base`, `conversations`, and `events` tables in Supabase.

### 3. Run Locally
```bash
uv run fastapi dev app/main.py        # Start API
uv run python -m app.poller          # Start Poller
```

### 4. Deploy with Docker
```bash
docker-compose up -d --build
```
