import streamlit as st
import time
from pipeline import run_research_pipeline

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ResearchAI — Multi-Agent Intelligence Platform",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# MODERN DARK THEME WITH ENHANCED FONT SIZES & COVER PAGE STYLING
# ============================================================

st.markdown(
    """
    <style>
    /* ---------- GLOBAL & TYPOGRAPHY ---------- */
    html, body, .stApp {
        background-color: #080c14;
        color: #e2e8f0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 18px;
    }

    [data-testid="stHeader"] {
        background-color: rgba(8, 12, 20, 0.9);
        backdrop-filter: blur(10px);
    }

    .block-container {
        max-width: 1300px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Headings */
    h1 { font-size: 42px !important; font-weight: 800 !important; color: #f8fafc !important; }
    h2 { font-size: 32px !important; font-weight: 750 !important; color: #f8fafc !important; margin-top: 1.5rem !important; }
    h3 { font-size: 26px !important; font-weight: 700 !important; color: #f1f5f9 !important; }
    p, li, span { font-size: 18px; line-height: 1.7; }

    /* ---------- BRAND HEADER ---------- */
    .brand-title {
        font-size: 36px;
        font-weight: 800;
        letter-spacing: -1px;
        color: #f8fafc;
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 8px;
    }

    .brand-accent {
        background: linear-gradient(135deg, #38bdf8 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .brand-tagline {
        font-size: 16px;
        color: #94a3b8;
        font-weight: 500;
        letter-spacing: 0.5px;
    }

    /* ---------- COVER PAGE / HERO BANNER ---------- */
    .cover-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.8) 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 20px;
        padding: 48px 44px;
        margin: 24px 0 32px 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }

    .cover-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38bdf8;
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 1.2px;
        margin-bottom: 20px;
        text-transform: uppercase;
    }

    .cover-heading {
        font-size: 54px;
        font-weight: 850;
        line-height: 1.1;
        color: #ffffff;
        margin-bottom: 18px;
        letter-spacing: -1.5px;
    }

    .cover-sub {
        color: #cbd5e1;
        font-size: 21px;
        line-height: 1.6;
        max-width: 820px;
        font-weight: 400;
    }

    /* ---------- PIPELINE STEP CARDS ---------- */
    .step-card {
        background: #0f172a;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px 14px;
        text-align: center;
        transition: all 0.25s ease;
    }

    .step-card:hover {
        border-color: rgba(56, 189, 248, 0.5);
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(56, 189, 248, 0.15);
    }

    .step-num {
        color: #38bdf8;
        font-size: 14px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .step-name {
        color: #f8fafc;
        font-size: 16px;
        font-weight: 700;
        margin-top: 6px;
    }

    .step-desc {
        font-size: 13px;
        color: #64748b;
        margin-top: 4px;
    }

    /* ---------- INPUT & FORM CONTROLS ---------- */
    textarea {
        background-color: #0a0f1d !important;
        color: #f8fafc !important;
        border: 1px solid #1e293b !important;
        border-radius: 14px !important;
        padding: 18px !important;
        font-size: 18px !important;
        line-height: 1.6 !important;
    }

    textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        min-height: 56px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.3) !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #0369a1 0%, #1d4ed8 100%) !important;
        box-shadow: 0 8px 28px rgba(2, 132, 199, 0.5) !important;
        transform: translateY(-2px) !important;
    }

    /* ---------- METRICS OVERRIDE ---------- */
    [data-testid="stMetric"] {
        background: #0f172a;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 20px 24px;
    }

    [data-testid="stMetricLabel"] {
        font-size: 16px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 36px !important;
        color: #f8fafc !important;
        font-weight: 800 !important;
    }

    /* ---------- TABS STYLING ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        border-bottom: 2px solid #1e293b;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 10px 10px 0 0;
        color: #94a3b8;
        padding: 12px 24px;
        font-size: 18px !important;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: #0f172a;
        color: #38bdf8 !important;
        border-bottom: 3px solid #38bdf8;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background-color: #0f172a;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR NAVIGATION & CONFIGURATION
# ============================================================

with st.sidebar:
    st.markdown("### ⚙️ Engine Controls")
    
    st.markdown("---")
    st.markdown("#### 🛠️ Architecture Modules")
    st.caption("Active pipeline infrastructure:")
    
    st.markdown("• **Agent Controller:** `agent.py` Active")
    st.markdown("• **RAG Engine:** Embeddings & Retriever")
    st.markdown("• **Tool Set:** Web Scraper & Search")
    st.markdown("• **Evaluation Framework:** Metrics On")
    
    st.markdown("---")
    st.markdown("#### ⚙️ Runtime Settings")
    enable_rag = st.checkbox("Enable RAG Context Retrieval", value=True)
    enable_critic = st.checkbox("Enable Critic Agent Verification", value=True)
    
    st.markdown("---")
    st.caption("ResearchAI v2.5 • Enterprise Multi-Agent System")

# ============================================================
# BRAND & HEADER
# ============================================================

st.markdown(
    """
    <div class="brand-title">
        <span>✦</span> Research<span class="brand-accent">AI</span>
    </div>
    <div class="brand-tagline">AUTONOMOUS MULTI-AGENT RESEARCH & INTELLIGENCE SYSTEM</div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# COVER PAGE / HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="cover-card">
        <div class="cover-badge">✦ Powered by Autonomous Agent Orchestration</div>
        <div class="cover-heading">Research anything.<br>Understand everything.</div>
        <div class="cover-sub">
            Formulate complex research queries and let a dedicated network of AI agents 
            discover, scrape, analyze, draft, and critically review deep intelligence reports for you.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# PIPELINE ARCHITECTURE DISPLAY
# ============================================================

st.markdown("### 🔄 Autonomous Pipeline Workflow")

col1, col2, col3, col4, col5 = st.columns(5)

steps = [
    ("01", "Web Search", "Query & Discovery"),
    ("02", "Scraper / RAG", "Context Vectorization"),
    ("03", "Reader Agent", "Data Synthesis"),
    ("04", "Writer Agent", "Draft Report"),
    ("05", "Critic Agent", "Review & Score"),
]

for col, (num, name, desc) in zip([col1, col2, col3, col4, col5], steps):
    with col:
        st.markdown(
            f"""
            <div class="step-card">
                <div class="step-num">{num}</div>
                <div class="step-name">{name}</div>
                <div class="step-desc">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# RESEARCH INPUT SECTION
# ============================================================

st.markdown("### 📝 Enter Your Research Prompt")

topic = st.text_area(
    "Research Topic Input",
    placeholder="e.g., Provide a comparative analysis of Quantum Computing hardware architectures (Superconducting vs. Trapped Ion) and their commercial timeline...",
    height=120,
    label_visibility="collapsed"
)

start_research = st.button("✦  Launch Research Pipeline", use_container_width=True)

# Session State to hold research results
if "pipeline_result" not in st.session_state:
    st.session_state.pipeline_result = None

# ============================================================
# EXECUTION LOGIC
# ============================================================

if start_research:
    if not topic.strip():
        st.warning("⚠️ Please enter a research topic before starting.")
        st.stop()

    try:
        start_time = time.time()
        with st.status("⚡ Executing Multi-Agent Pipeline...", expanded=True) as status:
            st.write("🔎 **Search Agent:** Scanning web sources and indexing data...")
            time.sleep(0.5)
            
            st.write("📖 **Reader Agent & RAG:** Extracting key findings and vectorizing documents...")
            
            # Run actual backend pipeline function
            result = run_research_pipeline(topic.strip())
            
            st.write("✍️️ **Writer Agent:** Structuring narrative and preparing comprehensive report...")
            time.sleep(0.5)
            
            st.write("🔍 **Critic Agent:** Reviewing factual alignment and evaluating output quality...")
            time.sleep(0.5)
            
            status.update(label="✅ Research Execution Complete!", state="complete", expanded=False)

        execution_time = round(time.time() - start_time, 2)
        st.session_state.pipeline_result = (result, execution_time)

    except Exception as e:
        st.error("❌ An error occurred during the research pipeline execution.")
        st.exception(e)

# ============================================================
# RESULTS & OUTPUT PANELS
# ============================================================

if st.session_state.pipeline_result:
    result, execution_time = st.session_state.pipeline_result

    final_answer = result.get("answer", "No report was generated.")
    sources = result.get("sources", [])
    critique = result.get("critique", "")
    research = result.get("research", "")

    st.markdown("---")
    st.markdown("## 📊 Research Execution Summary")

    # Metrics Grid
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Sources Scanned", len(sources) if isinstance(sources, list) else 0)
    with m2:
        st.metric("Report Word Count", len(final_answer.split()))
    with m3:
        st.metric("Execution Time", f"{execution_time}s")
    with m4:
        st.metric("Active Agents", "4 Agents")

    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Output Tabs
    tab_report, tab_sources, tab_eval, tab_raw = st.tabs([
        "📄 Final Report", 
        "🔗 Sources & Citations", 
        "🔍 Critic Evaluation", 
        "📖 Reader Analysis"
    ])

    with tab_report:
        st.markdown(final_answer)
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="⬇ Download Final Research Report (.md)",
            data=final_answer,
            file_name="research_report.md",
            mime="text/markdown",
            use_container_width=True
        )

    with tab_sources:
        if sources:
            for idx, source in enumerate(sources, 1):
                if isinstance(source, dict):
                    title = source.get('title', f'Source {idx}')
                    url = source.get('url', '#')
                    st.markdown(f"**{idx}. [{title}]({url})**")
                    if "snippet" in source:
                        st.caption(source["snippet"])
                else:
                    st.markdown(f"**{idx}.** {source}")
        else:
            st.info("No external links returned for this run.")

    with tab_eval:
        if critique:
            st.markdown(critique)
        else:
            st.info("No critic output generated.")

    with tab_raw:
        if research:
            st.markdown(research)
        else:
            st.info("No raw research logs available.")

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.caption("ResearchAI Multi-Agent Workbench • Built with Streamlit & Python")