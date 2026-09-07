# DriveWise AI 🚗

An AI-powered vehicle diagnostics assistant that helps Pakistani car owners identify likely problems from their symptoms, understand possible causes, and estimate repair costs in PKR — with optional AI analysis via a free Groq cloud API or a fully local Ollama model.

## Features

- **Symptom-based diagnosis** — Describe your car's problem and get matching diagnoses from a curated knowledge base of 40 entries covering 9 common symptom areas: engine overheating, engine shaking, exhaust smoke, low engine oil, poor fuel average, car AC not cooling, brake noise, suspension noise, and battery not starting.
- **Pakistan-market vehicles** — Includes common local models like Suzuki Alto, Toyota Corolla, and Honda Civic, with generic guidance that applies to any vehicle.
- **PKR repair cost estimates** — Each likely cause shows an estimated repair cost range in Pakistani Rupees.
- **AI analysis (optional)** — Streams a detailed second opinion from an AI provider: a free Groq cloud API (GPT-OSS 120B) when a key is configured, or a local Ollama model (`llama3.2:3b`) when running on your own machine. No sign-up required — knowledge-base diagnoses work without any AI setup.
- **Graceful AI failure handling** — If the AI provider is offline, errors out, or returns an empty response, the app shows a clear message with a retry button — the knowledge-base results always stay available.
- **Maintenance schedule** — Suggested service intervals for the selected vehicle.
- **Diagnosis history** — Session history in the sidebar lets you revisit earlier diagnoses.
- **Downloadable report** — Export any diagnosis as a plain-text report.

## Tech Stack

- [Python](https://www.python.org/) 3.11+
- [Streamlit](https://streamlit.io/) — web UI
- [pandas](https://pandas.pydata.org/) — knowledge-base data
- [requests](https://requests.readthedocs.io/) — AI provider API client
- [Groq](https://groq.com/) — free cloud LLM API (optional)
- [Ollama](https://ollama.com/) — local LLM runtime (optional)

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/DriveWise-AI.git
   cd DriveWise-AI
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:

   ```bash
   streamlit run app.py
   ```

The app opens at `http://localhost:8501`.

## Optional: Enable AI Analysis

Knowledge-base diagnoses work without any AI setup. The app automatically picks the first available provider:

1. **Groq cloud API** — if a `GROQ_API_KEY` is configured (free key, runs GPT-OSS 120B)
2. **Local Ollama** — if an Ollama server is reachable on your machine
3. **None** — the AI panel shows an unavailable message; knowledge-base results remain fully usable

### Option A: Groq cloud API (works on hosted deployments)

1. Create a free API key at [console.groq.com](https://console.groq.com) (no credit card required).
2. Configure the key:
   - **Locally:** create `.streamlit/secrets.toml` in the project root with:
     ```toml
     GROQ_API_KEY = "gsk_your_key_here"
     ```
   - **Streamlit Community Cloud:** open the app's settings → *Secrets* → add the same `GROQ_API_KEY` entry.
3. Re-run the app — the header shows "AI Assistant Ready — powered by Groq".

Note: in cloud mode the diagnosis prompt is sent to Groq's API. When running locally with Ollama, all analysis stays on your device.

### Option B: Local Ollama (fully private, on-device)

1. Install [Ollama](https://ollama.com/download).
2. Pull the model used by the app:

   ```bash
   ollama pull llama3.2:3b
   ```

3. Start Ollama (it usually runs automatically after installation) and re-run the app.

If no provider is available, the app shows an unavailable message with a **Retry AI Analysis** button — no crash, and knowledge-base results remain fully usable.

## Project Structure

```
DriveWise-AI/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── drivewise_ai/
│   └── diagnosis.py       # AI provider client (Groq + Ollama streaming)
├── data/
│   ├── cars.csv           # Vehicle catalog
│   └── issues.csv         # Issue knowledge base (symptoms, causes, fixes)
├── ui/
│   ├── components.py      # Reusable UI components and alerts
│   ├── maintenance.py     # Maintenance schedule section
│   └── styles.py          # CSS theme and styling
└── assets/                # Images
```

## How Diagnosis Works

1. Select your vehicle (brand, model, year, engine).
2. Describe the problem in your own words or pick a symptom chip.
3. DriveWise matches your description against the knowledge base and shows:
   - Likely causes with confidence levels
   - Estimated repair costs in PKR
   - A streaming AI analysis (if an AI provider is available)
4. Download the report or revisit the diagnosis from the sidebar history.

## Disclaimer

DriveWise AI provides guidance only. Always consult a qualified mechanic before making repair decisions.
