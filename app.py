import streamlit as st
import time
import html
from pipeline import run_research_pipeline

def e(text: str) -> str:
    """Escape text for safe injection into HTML."""
    return html.escape(str(text))

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Deep Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
}

.stApp {
    background-color: #0a0a0f;
    color: #e8e8f0;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3rem 4rem; max-width: 1100px; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(99,102,241,.18) 0%, transparent 70%);
    pointer-events: none;
}
.hero-tag {
    display: inline-block;
    font-size: .65rem;
    letter-spacing: .2em;
    text-transform: uppercase;
    color: #818cf8;
    border: 1px solid rgba(129,140,248,.3);
    padding: .25rem .75rem;
    border-radius: 2rem;
    margin-bottom: 1.25rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.6rem);
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, #e0e7ff 30%, #818cf8 70%, #6366f1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 .75rem;
}
.hero-sub {
    color: #6b7280;
    font-size: .85rem;
    letter-spacing: .04em;
}

/* ── Search box ── */
.stTextInput > div > div > input {
    background: #111118 !important;
    border: 1px solid rgba(99,102,241,.35) !important;
    border-radius: 8px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: .9rem !important;
    padding: .75rem 1.1rem !important;
    transition: border-color .2s, box-shadow .2s;
}
.stTextInput > div > div > input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,.15) !important;
}
.stTextInput > div > div > input::placeholder { color: #3f3f5a !important; }

/* ── Button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #4f46e5, #6366f1) !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: .85rem !important;
    letter-spacing: .06em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 8px !important;
    padding: .65rem 1.5rem !important;
    cursor: pointer !important;
    transition: opacity .2s, transform .15s !important;
}
.stButton > button:hover { opacity: .88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── Pipeline steps ── */
.step-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: .75rem;
    margin: 2rem 0 1.5rem;
}
.step-card {
    background: #111118;
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    transition: border-color .3s;
    position: relative;
    overflow: hidden;
}
.step-card.active {
    border-color: #6366f1;
    box-shadow: 0 0 18px rgba(99,102,241,.2);
}
.step-card.done {
    border-color: #10b981;
    box-shadow: 0 0 12px rgba(16,185,129,.1);
}
.step-card.active::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #6366f1, transparent);
    animation: shimmer 1.4s infinite;
}
@keyframes shimmer {
    0%  { transform: translateX(-100%); }
    100%{ transform: translateX(100%); }
}
.step-icon { font-size: 1.4rem; margin-bottom: .4rem; }
.step-label {
    font-family: 'Syne', sans-serif;
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: #4b5563;
}
.step-card.active .step-label { color: #818cf8; }
.step-card.done .step-label { color: #10b981; }

/* ── Result panels ── */
.panel {
    background: #0e0e16;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    margin-bottom: 1.25rem;
    overflow: hidden;
}
.panel-header {
    display: flex;
    align-items: center;
    gap: .6rem;
    padding: .85rem 1.2rem;
    border-bottom: 1px solid #1e1e2e;
    background: #111118;
}
.panel-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
}
.panel-title {
    font-family: 'Syne', sans-serif;
    font-size: .72rem;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
}
.panel-body {
    padding: 1.2rem;
    font-size: .8rem;
    line-height: 1.75;
    color: #9ca3af;
    max-height: 320px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
}
.panel-body::-webkit-scrollbar { width: 4px; }
.panel-body::-webkit-scrollbar-track { background: transparent; }
.panel-body::-webkit-scrollbar-thumb { background: #2d2d44; border-radius: 2px; }

/* ── Report panel (full height) ── */
.report-body {
    padding: 1.5rem 1.75rem;
    font-size: .85rem;
    line-height: 1.85;
    color: #d1d5db;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Feedback panel ── */
.feedback-body {
    padding: 1.2rem;
    font-size: .8rem;
    line-height: 1.75;
    color: #9ca3af;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Status bar ── */
.status-bar {
    display: flex;
    align-items: center;
    gap: .5rem;
    font-size: .72rem;
    color: #6b7280;
    letter-spacing: .04em;
    margin-bottom: 1rem;
}
.status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 6px #10b981;
}
.status-dot.running {
    background: #f59e0b;
    box-shadow: 0 0 6px #f59e0b;
    animation: pulse 1s infinite;
}
@keyframes pulse {
    0%,100% { opacity:1; } 50% { opacity:.4; }
}

/* ── Divider ── */
hr { border-color: #1e1e2e !important; margin: 2rem 0 !important; }

/* ── Error ── */
.err-box {
    background: rgba(239,68,68,.08);
    border: 1px solid rgba(239,68,68,.3);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    color: #f87171;
    font-size: .8rem;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">Multi-Agent System</div>
    <h1>Deep Research Agent</h1>
    <p class="hero-sub">Search → Scrape → Write → Critique &nbsp;|&nbsp; Powered by LangChain</p>
</div>
""", unsafe_allow_html=True)

# ── Input row ─────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])
with col_input:
    topic = st.text_input(
        label="topic",
        placeholder="e.g.  Quantum error correction in 2025",
        label_visibility="collapsed",
    )
with col_btn:
    st.markdown("<div style='margin-top:4px'>", unsafe_allow_html=True)
    run_clicked = st.button("Run →")
    st.markdown("</div>", unsafe_allow_html=True)

# ── Pipeline step cards (always visible) ─────────────────────────────────────
STEPS = [
    ("🔍", "Search"),
    ("📄", "Scrape"),
    ("✍️",  "Write"),
    ("🧠", "Critique"),
]

def render_steps(active: int = -1, done_up_to: int = -1):
    cols_html = ""
    for i, (icon, label) in enumerate(STEPS):
        if i < done_up_to:
            css = "done"
        elif i == active:
            css = "active"
        else:
            css = ""
        cols_html += f"""
        <div class="step-card {css}">
            <div class="step-icon">{icon}</div>
            <div class="step-label">{label}</div>
        </div>"""
    st.markdown(f'<div class="step-grid">{cols_html}</div>', unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = None
if "running" not in st.session_state:
    st.session_state.running = False

# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_clicked:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.running = True
        st.session_state.results = None

        # Step containers
        steps_placeholder = st.empty()
        status_placeholder = st.empty()

        def show_status(msg: str, running: bool = True):
            dot_class = "running" if running else ""
            status_placeholder.markdown(
                f'<div class="status-bar"><div class="status-dot {dot_class}"></div>{msg}</div>',
                unsafe_allow_html=True,
            )

        try:
            # ── Step 1 ─────────────────────────────────────────────────────
            with steps_placeholder:
                render_steps(active=0)
            show_status("Search agent querying the web…")
            
            from agents import build_search_agent
            from langchain_core.messages import HumanMessage

            search_agent = build_search_agent()
            search_result = search_agent.invoke(
                {"messages": [HumanMessage(content=f"Find recent, reliable and detailed information about: {topic}")]}
            )
            search_results = search_result["messages"][-1].content

            # ── Step 2 ─────────────────────────────────────────────────────
            with steps_placeholder:
                render_steps(active=1, done_up_to=1)
            show_status("Reader agent scraping top resources…")

            from agents import build_reader_agent
            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke(
                {"messages": [HumanMessage(
                    f'Based on the following search result about "{topic}",\n'
                    f'Pick the most relevent URL and scrape it for deeper content.\n\n'
                    f'Search Result:\n{search_results[:1000]}'
                )]}
            )
            scraped_content = reader_result["messages"][-1].content

            # ── Step 3 ─────────────────────────────────────────────────────
            with steps_placeholder:
                render_steps(active=2, done_up_to=2)
            show_status("Writer drafting the report…")

            from agents import writer_chain
            research_combined = (
                f"SEARCH RESULT:\n{search_results}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{scraped_content}"
            )
            report = writer_chain.invoke({"topic": topic, "research": research_combined})

            # ── Step 4 ─────────────────────────────────────────────────────
            with steps_placeholder:
                render_steps(active=3, done_up_to=3)
            show_status("Critic reviewing the report…")

            from agents import critic_chain
            feedback = critic_chain.invoke({"report": report})

            # ── Done ───────────────────────────────────────────────────────
            with steps_placeholder:
                render_steps(done_up_to=4)
            show_status("Research complete.", running=False)

            st.session_state.results = {
                "search_results": search_results,
                "scraped_content": scraped_content,
                "report": report,
                "feedback": feedback,
            }

        except Exception as e:
            st.markdown(f'<div class="err-box">⚠ Pipeline error: {e}</div>', unsafe_allow_html=True)

        st.session_state.running = False

# ── Idle step display ─────────────────────────────────────────────────────────
if not st.session_state.running and st.session_state.results is None:
    render_steps()

# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.results:
    r = st.session_state.results
    st.markdown("<hr>", unsafe_allow_html=True)

    # Search + Scrape side by side
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="panel">
            <div class="panel-header">
                <div class="panel-dot" style="background:#818cf8"></div>
                <span class="panel-title" style="color:#818cf8">Search Results</span>
            </div>
            <div class="panel-body">{e(r['search_results'])}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="panel">
            <div class="panel-header">
                <div class="panel-dot" style="background:#f59e0b"></div>
                <span class="panel-title" style="color:#f59e0b">Scraped Content</span>
            </div>
            <div class="panel-body">{e(r['scraped_content'])}</div>
        </div>
        """, unsafe_allow_html=True)

    # Full report
    st.markdown(f"""
    <div class="panel">
        <div class="panel-header">
            <div class="panel-dot" style="background:#10b981"></div>
            <span class="panel-title" style="color:#10b981">Final Research Report</span>
        </div>
        <div class="report-body">{e(r['report'])}</div>
    </div>
    """, unsafe_allow_html=True)

    # Critic feedback
    st.markdown(f"""
    <div class="panel">
        <div class="panel-header">
            <div class="panel-dot" style="background:#f43f5e"></div>
            <span class="panel-title" style="color:#f43f5e">Critic Feedback</span>
        </div>
        <div class="feedback-body">{e(r['feedback'])}</div>
    </div>
    """, unsafe_allow_html=True)

    # Download button
    st.download_button(
        label="⬇  Download Report (.txt)",
        data=r["report"],
        file_name=f"research_{topic[:40].replace(' ','_')}.txt",
        mime="text/plain",
    )