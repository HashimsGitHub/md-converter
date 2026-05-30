import streamlit as st
import io
import zipfile
from pathlib import Path
from markitdown import MarkItDown

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MD//CONVERTER",
    page_icon="⚡",
    layout="wide",
)

# ── PROFESSIONAL NEON CYBERPUNK CSS (High Contrast, Readable) ─────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,100..900;1,100..900&family=Space+Mono:wght@400;700&family=Orbitron:wght@400;500;600;700;800;900&display=swap');

* {
    box-sizing: border-box;
}

:root {
    --neon-cyan: #00f0ff;
    --neon-pink: #ff007f;
    --neon-purple: #b000ff;
    --neon-yellow: #ffe600;
    --deep-blue: #050a14;
    --deep-blue-card: #0a0f1e;
    --panel-glow: rgba(0, 240, 255, 0.15);
    --text-bright: #ffffff;
    --text-dim: #a0b8d4;
    --border-glow: 0 0 10px rgba(0, 240, 255, 0.3);
    --card-border: 1px solid rgba(0, 240, 255, 0.2);
    --glow-cyan: 0 0 8px #00f0ff, 0 0 20px rgba(0, 240, 255, 0.5);
    --glow-pink: 0 0 8px #ff007f, 0 0 20px rgba(255, 0, 127, 0.5);
    --glow-purple: 0 0 8px #b000ff, 0 0 20px rgba(176, 0, 255, 0.5);
}

/* Dark deep blue background - ensures no white areas */
html, body, .stApp, .stApp > header, .stApp > div, .main {
    background: #050a14 !important;
    background-color: #050a14 !important;
}

[data-testid="stAppViewContainer"] {
    background: #050a14 !important;
    background-image: radial-gradient(circle at 10% 20%, rgba(0, 240, 255, 0.03) 0%, #050a14 80%) !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {
    background: #050a14 !important;
}

/* Hide default Streamlit elements */
#MainMenu, footer, header {
    visibility: hidden;
}

/* Font overrides for readability */
h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown {
    color: var(--text-bright) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Monospace for code-like elements */
.code-font, .stDownloadButton button, .stButton button, .stFileUploader label {
    font-family: 'Space Mono', monospace !important;
}

/* Title styling */
.cyber-header {
    text-align: center;
    padding: 2rem 0 1rem;
    position: relative;
    margin-bottom: 1rem;
}

.cyber-title {
    font-family: 'Orbitron', monospace;
    font-size: 3rem;
    font-weight: 900;
    letter-spacing: 0.2em;
    background: linear-gradient(135deg, var(--neon-cyan), var(--neon-purple));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-shadow: none;
    margin: 0;
    line-height: 1.2;
}

.cyber-title span {
    background: linear-gradient(135deg, var(--neon-pink), var(--neon-yellow));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.cyber-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: var(--neon-cyan);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.5rem;
    opacity: 0.9;
}

/* Corner accents */
.corner-tl, .corner-tr, .corner-bl, .corner-br {
    position: absolute;
    width: 20px;
    height: 20px;
    border-color: var(--neon-cyan);
    border-style: solid;
    opacity: 0.8;
}

.corner-tl { top: 0; left: 0; border-width: 2px 0 0 2px; }
.corner-tr { top: 0; right: 0; border-width: 2px 2px 0 0; }
.corner-bl { bottom: 0; left: 0; border-width: 0 0 2px 2px; }
.corner-br { bottom: 0; right: 0; border-width: 0 2px 2px 0; }

/* Neon divider */
.cyber-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), var(--neon-pink), var(--neon-purple), transparent);
    margin: 1rem 0 2rem;
    box-shadow: 0 0 8px rgba(0, 240, 255, 0.5);
}

/* Format label */
.format-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    color: var(--neon-cyan);
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    border-left: 4px solid var(--neon-pink);
    padding-left: 1rem;
}

/* Radio buttons - high contrast */
div[data-testid="stRadio"] > div {
    display: flex !important;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 2rem;
}

div[data-testid="stRadio"] > div > label {
    background: rgba(10, 15, 30, 0.8) !important;
    border: 1px solid rgba(0, 240, 255, 0.3) !important;
    border-radius: 0px !important;
    padding: 0.7rem 1.8rem !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    color: #c0d4f0 !important;
    cursor: pointer;
    transition: all 0.25s ease;
    backdrop-filter: blur(4px);
}

div[data-testid="stRadio"] > div > label:hover {
    border-color: var(--neon-cyan) !important;
    color: var(--neon-cyan) !important;
    box-shadow: 0 0 12px rgba(0, 240, 255, 0.2) !important;
}

div[data-testid="stRadio"] > div > label[data-baseweb="radio"]:has(input:checked) {
    border-color: var(--neon-cyan) !important;
    background: rgba(0, 240, 255, 0.1) !important;
    color: var(--neon-cyan) !important;
    box-shadow: 0 0 20px rgba(0, 240, 255, 0.3) !important;
}

/* File uploader — force dark on every layer Streamlit renders */
div[data-testid="stFileUploader"],
div[data-testid="stFileUploader"] > div,
div[data-testid="stFileUploader"] section,
div[data-testid="stFileUploader"] section > div,
div[data-testid="stFileUploaderDropzone"],
div[data-testid="stFileUploaderDropzoneInstructions"] {
    background: #0a0f1e !important;
    background-color: #0a0f1e !important;
}

div[data-testid="stFileUploader"] {
    border: 2px dashed rgba(0, 240, 255, 0.5) !important;
    border-radius: 4px !important;
    transition: all 0.3s ease;
}

div[data-testid="stFileUploader"]:hover {
    border-color: var(--neon-cyan) !important;
    box-shadow: 0 0 20px rgba(0, 240, 255, 0.2) !important;
}

/* The drag-and-drop inner zone */
div[data-testid="stFileUploaderDropzone"] {
    border: none !important;
    padding: 1.5rem !important;
}

/* All text inside the uploader */
div[data-testid="stFileUploader"] label,
div[data-testid="stFileUploader"] span,
div[data-testid="stFileUploader"] p,
div[data-testid="stFileUploader"] small,
div[data-testid="stFileUploaderDropzoneInstructions"] span,
div[data-testid="stFileUploaderDropzoneInstructions"] p {
    font-family: 'Space Mono', monospace !important;
    color: var(--neon-cyan) !important;
    background: transparent !important;
}

/* File size / secondary hint text */
div[data-testid="stFileUploader"] small,
div[data-testid="stFileUploaderDropzoneInstructions"] small {
    color: rgba(0, 240, 255, 0.6) !important;
    font-size: 0.75rem !important;
}

/* Browse files button */
div[data-testid="stFileUploader"] button {
    background: transparent !important;
    border: 1px solid var(--neon-pink) !important;
    border-radius: 2px !important;
    color: var(--neon-pink) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    transition: all 0.2s;
}

div[data-testid="stFileUploader"] button:hover {
    background: var(--neon-pink) !important;
    color: #050a14 !important;
    box-shadow: var(--glow-pink) !important;
}

/* Uploaded file badges */
[data-testid="stFileUploaderFile"],
[data-testid="stFileUploaderFile"] > div {
    background: #0d1428 !important;
    border-left: 3px solid var(--neon-cyan) !important;
    border-radius: 0 !important;
}

[data-testid="stFileUploaderFileName"] {
    color: var(--neon-cyan) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
}

[data-testid="stFileUploaderFileData"] {
    color: rgba(0, 240, 255, 0.6) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
}

[data-testid="stFileUploaderDeleteBtn"] button {
    color: var(--neon-pink) !important;
    background: transparent !important;
    border: none !important;
}

/* Convert button */
div[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, rgba(0, 240, 255, 0.15), rgba(176, 0, 255, 0.15)) !important;
    border: 2px solid var(--neon-cyan) !important;
    color: var(--neon-cyan) !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.25em !important;
    padding: 1rem !important;
    border-radius: 4px !important;
    cursor: pointer;
    transition: all 0.3s ease;
    backdrop-filter: blur(4px);
    margin: 0.5rem 0;
}

div[data-testid="stButton"] > button:hover {
    background: var(--neon-cyan) !important;
    color: #050a14 !important;
    box-shadow: var(--glow-cyan) !important;
    transform: translateY(-2px);
}

/* Progress bar */
div[data-testid="stProgressBar"] > div {
    background: rgba(10, 15, 30, 0.8) !important;
    border-radius: 2px !important;
    border: 1px solid rgba(0, 240, 255, 0.3) !important;
    height: 8px !important;
}

div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-purple)) !important;
    border-radius: 2px !important;
    box-shadow: 0 0 10px var(--neon-cyan) !important;
}

/* Progress text */
div[data-testid="stProgressBar"] + div p {
    color: var(--neon-cyan) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
}

/* Stats strip */
.stats-strip {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
    background: rgba(10, 15, 30, 0.7);
    border: 1px solid rgba(0, 240, 255, 0.3);
    backdrop-filter: blur(8px);
    padding: 1rem 1.5rem;
    margin: 1.5rem 0;
    border-radius: 4px;
}

.stat-item {
    text-align: center;
    flex: 1;
    min-width: 80px;
}

.stat-val {
    font-family: 'Orbitron', monospace;
    font-size: 1.8rem;
    font-weight: 900;
    background: linear-gradient(135deg, var(--neon-cyan), var(--neon-purple));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    display: block;
    line-height: 1.2;
}

.stat-lbl {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    color: var(--neon-yellow);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.25rem;
    display: block;
}

/* Result cards */
.result-card {
    background: rgba(10, 15, 30, 0.8);
    border: 1px solid rgba(0, 240, 255, 0.2);
    border-left: 4px solid var(--neon-cyan);
    border-radius: 4px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    backdrop-filter: blur(4px);
    transition: all 0.2s ease;
}

.result-card:hover {
    border-left-color: var(--neon-pink);
    box-shadow: 0 0 15px rgba(0, 240, 255, 0.15);
}

.result-card.error {
    border-left-color: var(--neon-pink);
}

.result-filename {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--neon-cyan);
    word-break: break-word;
}

.result-card.error .result-filename {
    color: var(--neon-pink);
}

.result-meta {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--neon-yellow);
    margin-top: 0.25rem;
}

.result-err {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: var(--neon-pink);
    margin-top: 0.25rem;
}

/* Download buttons inside results */
div[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    border: 1px solid var(--neon-cyan) !important;
    border-radius: 2px !important;
    color: var(--neon-cyan) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    padding: 0.4rem 1rem !important;
    transition: all 0.2s ease;
    white-space: nowrap;
}

div[data-testid="stDownloadButton"] > button:hover {
    background: var(--neon-cyan) !important;
    color: #050a14 !important;
    box-shadow: var(--glow-cyan) !important;
}

/* Download all zip button wrapper */
.dl-all-wrap {
    margin-top: 1rem;
}

.dl-all-wrap div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, rgba(255, 0, 127, 0.15), rgba(0, 240, 255, 0.15)) !important;
    border: 2px solid var(--neon-pink) !important;
    color: var(--neon-pink) !important;
    width: 100%;
    padding: 0.8rem !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.2em !important;
}

.dl-all-wrap div[data-testid="stDownloadButton"] > button:hover {
    background: var(--neon-pink) !important;
    color: #050a14 !important;
    box-shadow: var(--glow-pink) !important;
}

/* Footer ticker */
.ticker {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-dim);
    text-align: center;
    border-top: 1px solid rgba(0, 240, 255, 0.3);
    padding-top: 1.5rem;
    margin-top: 2rem;
    letter-spacing: 0.1em;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #0a0f1e;
}

::-webkit-scrollbar-thumb {
    background: var(--neon-cyan);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--neon-pink);
}

/* Text selection */
::selection {
    background: rgba(0, 240, 255, 0.3);
    color: white;
}

/* Typography improvements for readability */
.stMarkdown p, .stMarkdown li {
    font-size: 0.95rem;
    line-height: 1.5;
    color: #e0ecff !important;
}

/* Custom container width */
.block-container {
    max-width: 1200px !important;
    padding: 2rem 2rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cyber-header">
  <div class="corner-tl"></div><div class="corner-tr"></div>
  <div class="corner-bl"></div><div class="corner-br"></div>
  <p class="cyber-title">MD<span>//</span>CONVERTER</p>
  <p class="cyber-sub">⚡ MICROSOFT MARKITDOWN • NEURAL DOCUMENT PROCESSOR ⚡</p>
</div>
<div class="cyber-divider"></div>
""", unsafe_allow_html=True)

# ── Format selector ───────────────────────────────────────────────────────────
st.markdown('<p class="format-label">▸ SELECT INPUT FORMAT</p>', unsafe_allow_html=True)

fmt = st.radio("format", ["PDF", "PPTX", "DOCX"], horizontal=True, label_visibility="collapsed")

ACCEPT_MAP = {"PDF": [".pdf"], "PPTX": [".pptx"], "DOCX": [".docx"]}

st.markdown("<br>", unsafe_allow_html=True)

# ── File uploader ─────────────────────────────────────────────────────────────
uploaded = st.file_uploader(
    f"📁 DROP FILES OR CLICK TO UPLOAD • SUPPORTED: {ACCEPT_MAP[fmt][0]} • MULTIPLE ALLOWED",
    type=ACCEPT_MAP[fmt],
    accept_multiple_files=True,
    key=f"uploader_{fmt}",
)

st.markdown("<br>", unsafe_allow_html=True)

# ── Convert button ────────────────────────────────────────────────────────────
convert_btn = st.button("⚡ INITIATE CONVERSION", use_container_width=True)

if convert_btn:
    if not uploaded:
        st.markdown(
            '<div class="result-card error"><div class="result-filename">⚠ NO FILES DETECTED. UPLOAD AT LEAST ONE FILE TO PROCEED.</div></div>',
            unsafe_allow_html=True,
        )
    else:
        md_tool = MarkItDown()
        results = []

        progress = st.progress(0, text="Initializing conversion matrix...")
        total = len(uploaded)

        for i, f in enumerate(uploaded):
            stem = Path(f.name).stem
            progress.progress(i / total, text=f"[{i+1}/{total}] Converting: {f.name}")
            try:
                raw = f.read()
                result = md_tool.convert_stream(
                    io.BytesIO(raw),
                    file_extension=Path(f.name).suffix.lower(),
                )
                results.append((stem, result.text_content.encode("utf-8"), None))
            except Exception as e:
                results.append((stem, None, str(e)))

        progress.progress(1.0, text="Conversion complete.")

        # ── Stats ──
        ok = [r for r in results if r[1] is not None]
        err = [r for r in results if r[1] is None]
        total_kb = sum(len(r[1]) for r in ok) // 1024

        st.markdown(
            f"""
            <div class="stats-strip">
              <div class="stat-item"><span class="stat-val">{total}</span><span class="stat-lbl">FILES INPUT</span></div>
              <div class="stat-item"><span class="stat-val">{len(ok)}</span><span class="stat-lbl">CONVERTED</span></div>
              <div class="stat-item"><span class="stat-val">{len(err)}</span><span class="stat-lbl">ERRORS</span></div>
              <div class="stat-item"><span class="stat-val">{total_kb} KB</span><span class="stat-lbl">MD OUTPUT</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Per-file result cards ──
        for stem, md_bytes, error in results:
            if error:
                st.markdown(
                    f"""
                    <div class="result-card error">
                      <div>
                        <div class="result-filename">✗ {stem}.md</div>
                        <div class="result-err">{error[:120]}</div>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                chars = len(md_bytes)
                lines = md_bytes.count(b"\n")
                col_info, col_dl = st.columns([4, 1])
                with col_info:
                    st.markdown(
                        f"""
                        <div class="result-card">
                          <div>
                            <div class="result-filename">✓ {stem}.md</div>
                            <div class="result-meta">{chars:,} chars • {lines:,} lines</div>
                          </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col_dl:
                    st.download_button(
                        "↓ SAVE",
                        data=md_bytes,
                        file_name=f"{stem}.md",
                        mime="text/markdown",
                        key=f"dl_{stem}",
                        use_container_width=True,
                    )

        # ── Download all ZIP ──
        if len(ok) > 1:
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
                for stem, md_bytes, _ in ok:
                    zf.writestr(f"{stem}.md", md_bytes)
            st.markdown('<div class="dl-all-wrap">', unsafe_allow_html=True)
            st.download_button(
                f"⚡ DOWNLOAD ALL {len(ok)} FILES AS .ZIP",
                data=zip_buf.getvalue(),
                file_name="converted_markdown.zip",
                mime="application/zip",
                use_container_width=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ticker">
  POWERED BY MICROSOFT MARKITDOWN • PDF • DOCX • PPTX • OUTPUT FORMAT: MARKDOWN (.MD) • SYSTEM ONLINE
</div>
""", unsafe_allow_html=True)