import streamlit as st
import sys
import os
from datetime import datetime
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

sys.path.append(os.path.dirname(__file__))
from app import run_pipeline

# ── Page config ──────────────────────────────────────────
st.set_page_config(
    page_title="StoryForge Agent",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0a0a0f; color: #e2e8f0; }

    .main-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a78bfa, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    .script-box {
        background: #111118;
        border: 1px solid #1e1e2e;
        border-left: 4px solid #7c3aed;
        border-radius: 8px;
        padding: 24px;
        font-size: 1.05rem;
        line-height: 1.9;
        color: #e2e8f0;
        white-space: pre-wrap;
        margin: 12px 0;
    }

    .history-card {
        background: #111118;
        border: 1px solid #1e1e2e;
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: border-color 0.2s;
    }

    .history-card:hover { border-color: #7c3aed; }

    .history-topic {
        font-weight: 700;
        color: #e2e8f0;
        font-size: 0.9rem;
    }

    .history-meta {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 4px;
    }

    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        margin-right: 6px;
    }

    .badge-platform {
        background: rgba(124,58,237,0.15);
        color: #a78bfa;
        border: 1px solid rgba(124,58,237,0.3);
    }

    .badge-tone {
        background: rgba(6,182,212,0.12);
        color: #67e8f9;
        border: 1px solid rgba(6,182,212,0.2);
    }

    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #06b6d4);
        color: white;
        border: none;
        padding: 12px;
        font-size: 0.95rem;
        font-weight: 700;
        border-radius: 8px;
        width: 100%;
    }

    .stButton > button:hover { opacity: 0.9; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Initialize session state ──────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "current_result" not in st.session_state:
    st.session_state.current_result = None

# ── Sidebar — Script History ──────────────────────────────
with st.sidebar:
    st.markdown("### 📚 Script History")
    st.caption(f"{len(st.session_state.history)} scripts generated")

    if not st.session_state.history:
        st.info("No scripts yet. Generate your first one!")
    else:
        # Clear history button
        if st.button("Clear History", use_container_width=True):
            st.session_state.history = []
            st.session_state.current_result = None
            st.rerun()

        st.divider()

        # Show history cards
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.container():
                st.markdown(f"""
                <div class="history-card">
                    <div class="history-topic">{item['topic']}</div>
                    <div class="history-meta">
                        <span class="badge badge-platform">{item['platform']}</span>
                        <span class="badge badge-tone">{item['tone']}</span>
                    </div>
                    <div class="history-meta">{item['timestamp']}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"Load", key=f"load_{i}", use_container_width=True):
                    st.session_state.current_result = item["result"]
                    st.rerun()

# ── Main Area ─────────────────────────────────────────────
st.markdown('<div class="main-title">StoryForge Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered YouTube Shorts & Instagram Reels script generator</div>', unsafe_allow_html=True)

st.divider()

# ── Input Section ─────────────────────────────────────────
st.markdown("### What is your video about?")

topic = st.text_input(
    label="Topic",
    placeholder="e.g. black holes, latest AI news, Python tips for beginners...",
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns(3)

with col1:
    platform = st.selectbox(
        "Platform",
        options=["youtube_shorts", "instagram_reels"],
        format_func=lambda x: "YouTube Shorts (60s)" if x == "youtube_shorts" else "Instagram Reels (30s)"
    )

with col2:
    tone = st.selectbox(
        "Tone",
        options=["educational", "funny", "dramatic", "casual"],
        format_func=lambda x: {
            "educational": "Educational",
            "funny": "Funny",
            "dramatic": "Dramatic",
            "casual": "Casual"
        }[x]
    )

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    generate_clicked = st.button("Generate Script", use_container_width=True)

# ── Generation Logic ──────────────────────────────────────
if generate_clicked:
    if not topic.strip():
        st.error("Please enter a topic first!")
    else:
        with st.spinner("Searching the web and generating your script..."):
            try:
                result = run_pipeline(
                    topic=topic.strip(),
                    platform=platform,
                    tone=tone
                )

                # Save to history
                st.session_state.history.append({
                    "topic": topic.strip(),
                    "platform": platform,
                    "tone": tone,
                    "timestamp": datetime.now().strftime("%b %d, %H:%M"),
                    "result": result
                })

                st.session_state.current_result = result
                st.rerun()

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

# ── Results ───────────────────────────────────────────────
if st.session_state.current_result:
    result = st.session_state.current_result

    st.success("Script generated successfully!")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Words", result.get("word_count", 0))
    with col2:
        st.metric("Duration", result.get("estimated_duration", "N/A"))
    with col3:
        st.metric("Sources", len(result.get("sources", [])))
    with col4:
        platform_display = "YT Shorts" if result.get("platform") == "YouTube Shorts" else "Reels"
        st.metric("Platform", platform_display)

    st.divider()

    # Two column layout for script + details
    left, right = st.columns([3, 2])

    with left:
        st.markdown("### Script")
        st.markdown(
            f'<div class="script-box">{result.get("script", "")}</div>',
            unsafe_allow_html=True
        )

        # Download
        script_text = f"""STORYFORGE AGENT - Generated Script
=====================================
Topic: {result.get('topic')}
Platform: {result.get('platform')}
Tone: {result.get('tone')}
Word Count: {result.get('word_count')}
Estimated Duration: {result.get('estimated_duration')}

SCRIPT:
-------
{result.get('script')}

SUGGESTED TITLES:
-----------------
{result.get('titles')}

HASHTAGS:
---------
{result.get('hashtags')}

SOURCES:
--------
{chr(10).join(result.get('sources', []))}
"""
        st.download_button(
            label="Download Script (.txt)",
            data=script_text.encode('utf-8'),
            file_name=f"storyforge_{result.get('topic','script').replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with right:
        # Titles
        st.markdown("### Suggested Titles")
        titles = result.get("titles", "").split("\n")
        for title in titles:
            if title.strip():
                st.info(title.strip())

        # Hashtags
        st.markdown("### Hashtags")
        st.code(result.get("hashtags", ""), language=None)

        # Sources
        st.markdown("### Sources Used")
        for url in result.get("sources", []):
            if url:
                st.markdown(f"- [{url[:50]}...]({url})")

        # Research summary
        with st.expander("View Research Summary"):
            st.write(result.get("search_summary", ""))

    st.divider()
    st.caption("Built with Groq + Tavily + Streamlit + FastMCP")