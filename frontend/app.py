import os
import httpx
import streamlit as st

st.set_page_config(page_title="Student Support", page_icon="🎓", layout="centered")
API_URL = os.getenv("SUPPORT_API_URL", "http://127.0.0.1:8000")

with st.sidebar:
    dark_mode = st.toggle("Dark mode", value=True, key="dark_mode")

palette = (
    {"bg": "#0C1714", "surface": "#13241E", "raised": "#1B3027", "border": "#2B463A",
     "text": "#E5F3EB", "muted": "#A2BCAF", "accent": "#79DCAA", "hover": "#254938"}
    if dark_mode else
    {"bg": "#F5F8F6", "surface": "#FFFFFF", "raised": "#EDF5F0", "border": "#D7E5DC",
     "text": "#19372A", "muted": "#526F60", "accent": "#167447", "hover": "#E1F2E7"}
)
theme_css = ":root {" + "".join(f"--support-{key}: {value};" for key, value in palette.items()) + "}"
st.markdown("<style>" + theme_css + "</style>", unsafe_allow_html=True)

st.markdown("""
<style>
    .stApp { --background-color: var(--support-bg); --secondary-background-color: var(--support-surface);
        --text-color: var(--support-text); --primary-color: var(--support-accent); }
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"],
    [data-testid="stBottom"], [data-testid="stBottomBlockContainer"] {
        background: var(--support-bg); color: var(--support-text); color-scheme: normal;
    }
    [data-testid="stHeader"] { background: var(--support-bg); }
    [data-testid="stSidebar"] { background: var(--support-surface); color: var(--support-text); }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5,
    [data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"] {
        color: var(--support-text);
    }
    [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p { color: var(--support-muted); }
    [data-testid="stBottom"] > div,
    [data-testid="stBottom"] [data-testid="stVerticalBlock"] { background: var(--support-bg); }
    .stApp a { color: var(--support-accent); }
    .stApp hr { border-color: var(--support-border); }
    .stButton > button, .stLinkButton > a {
        background: var(--support-surface); color: var(--support-text);
        border: 1px solid var(--support-border);
    }
    .stButton > button:hover, .stLinkButton > a:hover {
        background: var(--support-hover); color: var(--support-accent);
        border-color: var(--support-accent);
    }
    .stButton > button:focus-visible { outline: 2px solid var(--support-accent); outline-offset: 3px; }
    [data-testid="stChatInput"], [data-testid="stChatInput"] > div {
        background: var(--support-raised); border-color: var(--support-border);
    }
    [data-testid="stChatInput"] textarea { color: var(--support-text); caret-color: var(--support-accent); }
    [data-testid="stChatInput"] textarea::placeholder { color: var(--support-muted); opacity: 1; }
    [data-testid="stChatInput"] button { color: var(--support-accent); }
    [data-testid="stChatInput"] button:disabled { color: var(--support-muted); opacity: .5; }
    [data-testid="stExpander"] { background: var(--support-surface); border-color: var(--support-border); }
    .stApp pre, .stApp code { background: var(--support-raised); color: var(--support-text); }
    [data-testid="stChatMessage"] { background: var(--support-surface); }
    .block-container { max-width: 960px; padding-top: 2.8rem; padding-bottom: 3rem; }
    h1 { letter-spacing: -0.045em; font-weight: 750 !important; }
    h3 { letter-spacing: -0.02em; }
    [data-testid="stSidebar"] { border-right: 1px solid var(--support-border); }
    [data-testid="stSidebar"] .block-container { padding-top: 2rem; }
    .eyebrow { color: var(--support-accent); font-size: .74rem; font-weight: 750;
        letter-spacing: .14em; margin-bottom: .4rem; }
    .intro { color: var(--support-muted); font-size: 1.08rem; line-height: 1.7;
        max-width: 620px; margin-bottom: 1.7rem; }
    .support-card { background: var(--support-surface); border: 1px solid var(--support-border);
        border-radius: 16px; padding: 1.2rem; min-height: 154px; }
    .support-card .icon { color: var(--support-accent); font-size: 1.35rem; margin-bottom: .6rem; }
    .support-card strong { display: block; font-size: .98rem; margin-bottom: .35rem; }
    .support-card p { color: var(--support-muted); font-size: .88rem; line-height: 1.6; margin: 0; }
    .team-item { padding: .75rem 0; border-bottom: 1px solid var(--support-border); }
    .team-item strong { font-size: .92rem; }
    .team-item p { color: var(--support-muted); font-size: .82rem; line-height: 1.6; margin: .25rem 0; }
    [data-testid="stChatMessage"] { border: 1px solid var(--support-border);
        border-radius: 18px; padding: 1.25rem; margin-bottom: 1rem; }
    [data-testid="stChatInput"] { border-radius: 16px; }
    .stButton > button { border-radius: 10px; }
    @media (max-width: 640px) {
        .block-container { padding-top: 1.5rem; }
        .support-card { min-height: auto; margin-bottom: .5rem; }
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<div class="eyebrow">YOUR US STUDENT JOURNEY, SUPPORTED</div>', unsafe_allow_html=True)
st.title("Student Support")
st.markdown('<p class="intro">Planning to study in the USA? Get help with F-1 visa preparation, '
            'your next application, or the interview ahead.</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🎓 Student Support")
    st.caption("A place to ask. A way forward.")
    st.divider()
    st.markdown("##### Meet your support team")
    for icon, name, description in [
        ("◎", "Orchestrator", "Finds the right specialist for your question."),
        ("✈", "Visa Support", "US F-1 preparation grounded in official source summaries."),
        ("↗", "Career Support", "Practical help with CVs, applications and interviews."),
    ]:
        st.markdown(f'<div class="team-item"><strong>{icon} &nbsp; {name}</strong>'
                    f'<p>{description}</p></div>', unsafe_allow_html=True)
    st.write("")
    st.caption("CONNECTION")
    if st.button("Check backend", use_container_width=True):
        try:
            with httpx.Client(timeout=10, trust_env=False) as client:
                response = client.get(f"{API_URL}/health")
                response.raise_for_status()
            health = response.json()
            st.success(f"Connected: {health['model']}")
            st.write(f"Visa source chunks: {health['visa_chunks']}")
        except (httpx.HTTPError, ValueError, KeyError):
            st.error("Backend or Ollama is unavailable. Check both services.")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("Powered by IBM Granite · Local Ollama")
    st.caption("Keep personal details private. Avoid sharing passport numbers or sensitive documents.")

suggestion = None
if not st.session_state.messages:
    columns = st.columns(3)
    cards = [
        ("✈", "US visa guidance", "Prepare for your F-1 application with official sources.",
         "What documents should I prepare for my US F-1 visa interview?"),
        ("↗", "Career confidence", "Turn your experience into a stronger application.",
         "How can I improve my CV when I have no work experience?"),
        ("✦", "Interview ready", "Prepare your examples and practise your approach.",
         "How should I prepare for a graduate software engineering interview?"),
    ]
    for column, (icon, title, description, question) in zip(columns, cards):
        with column:
            st.markdown(f'<div class="support-card"><div class="icon">{icon}</div>'
                        f'<strong>{title}</strong><p>{description}</p></div>', unsafe_allow_html=True)
            if st.button("Try a question", key=title, use_container_width=True):
                suggestion = question
    st.write("")
    st.caption("USA focus · F-1 application and DS-160 summaries · Sources reviewed 30 October 2026")
    with st.expander("What can visa support help with?"):
        st.write("Ask about F-1 application preparation, interview documents and DS-160. "
                 "Employment rules, CPT/OPT, status and travel are not yet covered by the source pack.")
        st.link_button("Official US student visa guide", "https://travel.state.gov/content/travel/en/us-visas/study/student-visa.html")

st.divider()
st.markdown("##### Your conversation")
st.caption("Ask one complete question at a time. Each answer is independent of earlier messages.")


def show(message):
    with st.chat_message(message["role"], avatar="🎓" if message["role"] == "assistant" else "👤"):
        if message.get("agent"):
            label = {"visa": "Visa Support", "career": "Career Support", "clarify": "Orchestrator"}
            st.caption(f"{label.get(message['agent'], 'Student Support')} · {message['model']}")
        st.markdown(message["content"])
        for source in message.get("citations", []):
            with st.expander(f"[{source['id']}] {source['title']}"):
                st.link_button("Open source", source["url"])
                st.caption(f"Reviewed: {source['reviewed']}")
                st.text(source["excerpt"])


for message in st.session_state.messages:
    show(message)

typed_prompt = st.chat_input("Ask about visas, careers or your next interview…", max_chars=8000)
if prompt := (typed_prompt or suggestion):
    user_message = {"role": "user", "content": prompt}
    st.session_state.messages.append(user_message)
    show(user_message)
    try:
        with st.spinner("Your support team is working…"):
            with httpx.Client(timeout=400, trust_env=False) as client:
                response = client.post(f"{API_URL}/chat", json={"message": prompt})
                response.raise_for_status()
            result = response.json()
        answer = {"role": "assistant", "content": result["answer"],
                  "agent": result["agent"], "model": result["model"], "citations": result["citations"]}
        st.session_state.messages.append(answer)
        show(answer)
    except (httpx.HTTPError, ValueError, KeyError):
        st.error("The request could not be completed. Check that FastAPI and Ollama are running, then submit your question again.")
