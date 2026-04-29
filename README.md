<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Syne&weight=800&size=32&pause=1000&color=6366F1&center=true&vCenter=true&width=600&lines=Deep+Research+Agent+🔬;Multi-Agent+AI+Research+System" alt="Typing SVG" />

<br/>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white"/>
  <img src="https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white"/>
</p>

<p align="center">
  A production-grade <strong>multi-agent AI research system</strong> that autonomously searches the web,<br/>
  scrapes top sources, writes structured reports, and critiques them — end to end.
</p>

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%"/>

</div>

<br/>

## 🧠 How It Works

```
 Your Topic
     │
     ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  🔍 Search  │────▶│  📄 Scrape  │────▶│  ✍️  Write  │────▶│  🧠 Critic  │
│    Agent    │     │    Agent    │     │    Chain    │     │    Chain    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
  Finds recent        Scrapes top          Drafts a           Reviews &
  web sources         URLs for             structured         scores the
  on your topic       deep content         report             report
```

<br/>

## ✨ Features

<table>
  <tr>
    <td>🔍</td>
    <td><strong>Autonomous Web Search</strong></td>
    <td>Search agent finds recent, reliable sources on any topic</td>
  </tr>
  <tr>
    <td>📄</td>
    <td><strong>Deep URL Scraping</strong></td>
    <td>Reader agent picks the most relevant URL and extracts full content</td>
  </tr>
  <tr>
    <td>✍️</td>
    <td><strong>Structured Report Writing</strong></td>
    <td>Writer chain produces Introduction → Key Findings → Conclusion → Sources</td>
  </tr>
  <tr>
    <td>🧠</td>
    <td><strong>AI Critic Review</strong></td>
    <td>Critic chain scores the report and gives actionable feedback</td>
  </tr>
  <tr>
    <td>🖥️</td>
    <td><strong>Streamlit UI</strong></td>
    <td>Live step-by-step progress, results panels, and report download</td>
  </tr>
  <tr>
    <td>⚡</td>
    <td><strong>Powered by Groq</strong></td>
    <td>Blazing fast inference using LLaMA 3.1 on Groq's LPU hardware</td>
  </tr>
</table>

<br/>

## 🗂️ Project Structure

```
deep-research-agent/
│
├── app.py              # Streamlit UI — live pipeline progress & results
├── pipeline.py         # Orchestrates all 4 agents in sequence
├── agents.py           # Search agent, Reader agent, Writer & Critic chains
├── tools.py            # web_search and scrape_url tool definitions
├── requirements.txt    # Python dependencies
└── .env                # API keys (never commit this!)
```

<br/>

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/ItsMukundKumar/deep-research-agent.git
cd deep-research-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your `.env` file

```env
GROQ_API_KEY=your_groq_api_key_here
```

> Get your free Groq API key at [console.groq.com](https://console.groq.com)

### 5. Run the app

```bash
streamlit run app.py
```

<br/>

## 🖥️ UI Preview

<div align="center">

| Step Cards | Live Progress | Results |
|:---:|:---:|:---:|
| Animated pipeline steps | Real-time status updates | Scrollable panels per agent |

</div>

<br/>

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|---|---|
| **LLM** | LLaMA 3.1 8B via Groq |
| **Agent Framework** | LangChain Core |
| **Tool Calling** | Custom `SimpleToolAgent` with `bind_tools` |
| **Web Search** | Brave Search API |
| **Scraping** | BeautifulSoup / requests |
| **UI** | Streamlit |
| **Env Management** | python-dotenv |

</div>

<br/>

## ☁️ Deployment

This app is deployable on **Streamlit Community Cloud** for free:

1. Push your repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New App**
3. Select your repo and set main file to `app.py`
4. Add `GROQ_API_KEY` under **Advanced Settings → Secrets**
5. Click **Deploy** ✅

<br/>

## ⚠️ Notes

- The free Groq tier has **token-per-minute limits** — if you hit a 429 error, wait a few seconds and retry
- Never commit your `.env` file — add it to `.gitignore`
- The pipeline makes sequential LLM calls, so complex topics may take 20–40 seconds

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%"/>

<div align="center">

<br/>

Made with ❤️ by [Mukund Kumar](https://github.com/ItsMukundKumar)

<br/>

⭐ **Star this repo if you found it useful!**

</div>