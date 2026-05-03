import streamlit as st
import requests
import base64
import time

st.set_page_config(page_title="DocMind AI", page_icon="🧠", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=DM+Sans:wght@400;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #080810 !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"], #MainMenu, footer, header { display: none !important; }

.top-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.2rem;
    font-weight: 900;
    background: linear-gradient(90deg, #818cf8, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 2px;
    text-align: center;
    padding: 36px 0 6px 0;
}
.top-sub {
    color: #475569;
    font-size: 0.78rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 28px;
}
.agent-row { display: flex; gap: 12px; margin-bottom: 16px; }
.agent-box {
    flex: 1; background: #0e0e1a;
    border: 1px solid #1e1e32; border-radius: 12px;
    padding: 14px; text-align: center;
}
.agent-emoji { font-size: 1.5rem; }
.agent-name { font-size: 0.85rem; font-weight: 600; color: #818cf8; margin-top: 4px; }
.agent-desc { font-size: 0.7rem; color: #475569; margin-top: 2px; }

.card { background: #0e0e1a; border: 1px solid #1e1e32; border-radius: 14px; padding: 20px 24px; margin-bottom: 16px; }
.card-title { font-size: 0.68rem; letter-spacing: 3px; text-transform: uppercase; color: #334155; margin-bottom: 12px; }

.step-row { display: flex; align-items: center; gap: 10px; padding: 8px 0; border-bottom: 1px solid #1e1e32; }
.step-row:last-child { border-bottom: none; }
.step-dot { width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; flex-shrink: 0; }
.dot-done { background: #34d399; color: #080810; }
.dot-active { background: #818cf8; color: white; animation: glow 1.2s infinite; }
.dot-wait { background: #1e1e32; color: #475569; }
@keyframes glow { 0%,100% { box-shadow: 0 0 0 0 #818cf840; } 50% { box-shadow: 0 0 0 8px #818cf810; } }
.step-label { font-size: 0.88rem; color: #94a3b8; }
.step-label.active { color: #818cf8; font-weight: 600; }
.step-label.done { color: #34d399; }

.result-box {
    background: #0e0e1a; border: 1px solid #1e1e32;
    border-top: 3px solid #818cf8; border-radius: 14px;
    padding: 24px 28px; margin-top: 16px;
    line-height: 1.8; color: #cbd5e1; font-size: 0.95rem;
}
.stButton > button {
    background: linear-gradient(135deg, #818cf8, #4f46e5) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important;
    font-size: 1rem !important; padding: 12px 0 !important;
    width: 100% !important; transition: all 0.2s !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 20px #818cf840 !important; }
[data-testid="stFileUploader"] { background: #0e0e1a !important; border: 2px dashed #1e1e32 !important; border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="top-title">🧠 DocMind AI</div>', unsafe_allow_html=True)
st.markdown('<div class="top-sub">Agentic PDF Review · CrewAI + Groq</div>', unsafe_allow_html=True)

st.markdown("""
<div class="agent-row">
    <div class="agent-box">
        <div class="agent-emoji">✍️</div>
        <div class="agent-name">Writer Agent</div>
        <div class="agent-desc">PDF Summary Specialist</div>
    </div>
    <div class="agent-box">
        <div class="agent-emoji">🔍</div>
        <div class="agent-name">Critic Agent</div>
        <div class="agent-desc">Review & Quality Control</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="card"><div class="card-title">📤 Upload PDF Document</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    size = f"{len(uploaded_file.getvalue())/1024:.1f} KB"
    st.markdown(f"""
    <div style="background:#0e0e1a;border:1px solid #818cf840;border-radius:10px;
                padding:12px 18px;margin-bottom:16px;font-size:0.85rem;color:#818cf8;">
        📄 <b>{uploaded_file.name}</b>
        <span style="color:#475569;margin-left:12px;font-size:0.75rem;">{size}</span>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("👁️ Preview PDF"):
        b64 = base64.b64encode(uploaded_file.getvalue()).decode()
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="400px"'
            f' style="border-radius:8px;border:1px solid #1e1e32;"></iframe>',
            unsafe_allow_html=True
        )

    if st.button("🚀 Start AI Review"):
        steps = [
            "📄 Extracting PDF Text",
            "✍️ Writer Agent — Summarizing",
            "🔍 Critic Agent — Reviewing",
            "✅ Output Ready"
        ]
        box = st.empty()

        for i in range(len(steps)):
            html = '<div class="card"><div class="card-title">⚙️ Pipeline</div>'
            for j, s in enumerate(steps):
                if j < i:
                    dot, lbl, icon = "dot-done", "done", "✓"
                elif j == i:
                    dot, lbl, icon = "dot-active", "active", "●"
                else:
                    dot, lbl, icon = "dot-wait", "", str(j+1)
                html += (
                    f'<div class="step-row">'
                    f'<div class="step-dot {dot}">{icon}</div>'
                    f'<div class="step-label {lbl}">{s}</div>'
                    f'</div>'
                )
            html += "</div>"
            box.markdown(html, unsafe_allow_html=True)
            time.sleep(0.7)

        try:
            uploaded_file.seek(0)
            res = requests.post(
                "http://127.0.0.1:8000/process",
                files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
                timeout=300
            )
            data = res.json()

            # All steps done
            html = '<div class="card"><div class="card-title">⚙️ Pipeline</div>'
            for s in steps:
                html += (
                    f'<div class="step-row">'
                    f'<div class="step-dot dot-done">✓</div>'
                    f'<div class="step-label done">{s}</div>'
                    f'</div>'
                )
            html += "</div>"
            box.markdown(html, unsafe_allow_html=True)

            if "result" in data:
                st.markdown(
                    f'<div class="result-box">'
                    f'🧠 <b style="color:#818cf8;">AI Review Result</b><br><br>'
                    f'{data["result"]}'
                    f'</div>',
                    unsafe_allow_html=True
                )
                b64r = base64.b64encode(data["result"].encode()).decode()
                fname = uploaded_file.name.replace(".pdf", "_review.txt")
                st.markdown(
                    f'<div style="margin-top:16px;text-align:center;">'
                    f'<a href="data:text/plain;base64,{b64r}" download="{fname}"'
                    f' style="background:linear-gradient(135deg,#818cf8,#4f46e5);color:white;'
                    f'padding:10px 28px;border-radius:8px;font-weight:600;'
                    f'text-decoration:none;font-size:0.9rem;">⬇️ Download Result</a>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                st.balloons()

            elif "error" in data:
                st.error(f"Backend Error: {data['error']}")

        except Exception as e:
            st.error(f"Error: {str(e)}")