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

# ── CSS: ported exactly from the DeepSeek HTML design ─────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

* { box-sizing: border-box; }

:root {
    --neon-cyan:      #00ffe7;
    --neon-pink:      #ff2d78;
    --neon-yellow:    #f5e642;
    --dark-bg:        #030612;
    --panel-bg:       #0a1022;
    --panel-border:   #142c4a;
    --text-main:      #c8d8f0;
    --text-dim:       #3c5a7a;
    --glow-cyan:      0 0 6px #00ffe7, 0 0 15px rgba(0,255,231,0.6);
    --glow-pink:      0 0 6px #ff2d78, 0 0 15px rgba(255,45,120,0.6);
    --glow-cyan-soft: 0 0 4px #00ffe7, 0 0 8px rgba(0,255,231,0.4);
}

/* ── Force black bg regardless of browser/OS theme ── */
html {
    background: #030612 !important;
}
body, [data-testid="stAppViewContainer"], [data-testid="stApp"],
[data-testid="stMain"], .main, section.main,
[class*="css"] {
    font-family: 'Rajdhani', sans-serif !important;
    background: #030612 !important;
    background-color: #030612 !important;
    color: var(--text-main) !important;
}
/* Sidebar & all wrappers */
[data-testid="stSidebar"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stBottom"] {
    background: #030612 !important;
    background-color: #030612 !important;
}
/* Radial gradient injected via pseudo on the main container */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background: radial-gradient(circle at 20% 30%, #050b1a 0%, #030612 60%);
    pointer-events: none;
    z-index: 0;
}
/* scanlines */
[data-testid="stAppViewContainer"]::after {
    content: "";
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent, transparent 2px,
        rgba(0,255,231,0.018) 2px, rgba(0,255,231,0.018) 4px
    );
    pointer-events: none;
    z-index: 1;
}

#MainMenu, footer, header { visibility: hidden; }

/* ── Full-width centered content column ── */
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
    width: 100% !important;
    position: relative;
    z-index: 2;
}
/* Inner content wrapper — centered column, max 900px */
.block-container > div:first-child {
    max-width: 900px !important;
    margin: 0 auto !important;
    padding: 0.5rem 1.5rem 3rem !important;
}

/* ── Header ── */
.cyber-header {
    text-align: center;
    padding: 2rem 0 1rem;
    position: relative;
    margin-bottom: 0.5rem;
}
.cyber-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.8rem;
    font-weight: 900;
    letter-spacing: 0.15em;
    color: var(--neon-cyan);
    text-shadow: var(--glow-cyan);
    margin: 0; line-height: 1;
}
.cyber-title span { color: var(--neon-pink); text-shadow: var(--glow-pink); }
.cyber-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-dim);
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-top: 0.6rem;
}
.corner-tl, .corner-tr, .corner-bl, .corner-br {
    position: absolute; width: 18px; height: 18px;
    border-color: var(--neon-cyan); border-style: solid; opacity: 0.7;
}
.corner-tl { top:0; left:0;  border-width: 2px 0 0 2px; }
.corner-tr { top:0; right:0; border-width: 2px 2px 0 0; }
.corner-bl { bottom:0; left:0;  border-width: 0 0 2px 2px; }
.corner-br { bottom:0; right:0; border-width: 0 2px 2px 0; }

.cyber-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), var(--neon-pink), transparent);
    margin: 1rem 0 2rem;
    opacity: 0.65;
}

/* ── Format label ── */
.format-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    color: var(--neon-cyan);
    text-transform: uppercase;
    margin-bottom: 0.7rem;
    border-left: 3px solid var(--neon-pink);
    padding-left: 0.75rem;
}

/* ── Radio buttons ── */
div[data-testid="stRadio"] label { display: none !important; }
div[data-testid="stRadio"] > div {
    display: flex !important;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-bottom: 1.8rem;
}
div[data-testid="stRadio"] > div > label {
    display: flex !important;
    align-items: center;
    gap: 0.4rem;
    background: var(--panel-bg) !important;
    border: 1px solid var(--panel-border) !important;
    padding: 0.6rem 1.5rem !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    color: var(--text-dim) !important;
    cursor: pointer;
    transition: all 0.2s;
    text-transform: uppercase;
    border-radius: 0 !important;
}
div[data-testid="stRadio"] > div > label:hover {
    color: var(--neon-cyan) !important;
    border-color: var(--neon-cyan) !important;
}
div[data-testid="stRadio"] > div > label:has(input:checked) {
    color: var(--neon-cyan) !important;
    border-color: var(--neon-cyan) !important;
    box-shadow: inset 0 0 12px rgba(0,255,231,0.1), var(--glow-cyan-soft) !important;
}
div[data-testid="stRadio"] > div > label > div:first-child { display: none !important; }

/* ── File uploader ── */
div[data-testid="stFileUploader"] {
    border: 1px dashed var(--neon-pink) !important;
    background: var(--panel-bg) !important;
    border-radius: 0 !important;
    padding: 1.8rem 1rem !important;
    text-align: center;
    transition: border 0.2s, box-shadow 0.2s;
}
div[data-testid="stFileUploader"]:hover {
    border-color: var(--neon-cyan) !important;
    box-shadow: var(--glow-cyan-soft) !important;
}
div[data-testid="stFileUploader"] section {
    border: none !important;
    background: transparent !important;
    padding: 0 !important;
}
div[data-testid="stFileUploader"] label {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.85rem !important;
    color: var(--text-dim) !important;
    letter-spacing: 0.1em !important;
}
div[data-testid="stFileUploader"] button {
    background: transparent !important;
    border: 1px solid var(--neon-pink) !important;
    color: var(--neon-pink) !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.15em !important;
    border-radius: 0 !important;
    padding: 0.4rem 1rem !important;
    transition: all 0.2s;
}
div[data-testid="stFileUploader"] button:hover {
    background: var(--neon-pink) !important;
    color: var(--dark-bg) !important;
    box-shadow: var(--glow-pink) !important;
}

/* ── File badges (uploaded file pills) ── */
div[data-testid="stFileUploaderDeleteBtn"] button {
    background: none !important;
    border: none !important;
    color: var(--neon-pink) !important;
    padding: 0 !important;
}
[data-testid="stFileUploaderFile"] {
    background: var(--panel-bg) !important;
    border-left: 3px solid var(--neon-cyan) !important;
    border-radius: 0 !important;
    padding: 0.3rem 0.8rem !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.7rem !important;
    color: var(--text-main) !important;
}

/* ── Progress bar ── */
div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-pink)) !important;
    box-shadow: var(--glow-cyan-soft) !important;
}
div[data-testid="stProgressBar"] > div {
    background: var(--panel-bg) !important;
    border: 1px solid var(--panel-border) !important;
    border-radius: 0 !important;
    height: 6px !important;
}

/* ── Convert button ── */
div[data-testid="stButton"] > button {
    width: 100%;
    background: transparent !important;
    border: 2px solid var(--neon-cyan) !important;
    color: var(--neon-cyan) !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.25em !important;
    padding: 0.8rem 2rem !important;
    border-radius: 0 !important;
    transition: all 0.2s;
    text-transform: uppercase;
}
div[data-testid="stButton"] > button:hover {
    background: var(--neon-cyan) !important;
    color: var(--dark-bg) !important;
    box-shadow: var(--glow-cyan) !important;
}

/* ── Download buttons ── */
div[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    border: 1px solid var(--neon-cyan) !important;
    color: var(--neon-cyan) !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.15em !important;
    border-radius: 0 !important;
    padding: 0.3rem 0.8rem !important;
    transition: all 0.2s;
    white-space: nowrap;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: var(--neon-cyan) !important;
    color: var(--dark-bg) !important;
    box-shadow: var(--glow-cyan-soft) !important;
}

/* ── Stats strip ── */
.stats-strip {
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
    background: var(--panel-bg);
    border: 1px solid var(--panel-border);
    padding: 0.8rem 1.2rem;
    margin-top: 1.5rem;
}
.stat-item { text-align: center; }
.stat-val {
    font-family: 'Orbitron', monospace;
    font-size: 1.3rem;
    font-weight: 900;
    color: var(--neon-cyan);
    text-shadow: var(--glow-cyan);
    display: block;
}
.stat-lbl {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.6rem;
    color: var(--text-dim);
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

/* ── Result cards ── */
.result-card {
    background: var(--panel-bg);
    border: 1px solid var(--panel-border);
    border-left: 3px solid var(--neon-cyan);
    padding: 0.7rem 1rem;
    margin: 0.4rem 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}
.result-card.error { border-left-color: var(--neon-pink); }
.result-filename {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    color: var(--neon-cyan);
    word-break: break-all;
}
.result-card.error .result-filename { color: var(--neon-pink); }
.result-meta {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.68rem;
    color: var(--text-dim);
    white-space: nowrap;
}
.result-err {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: var(--neon-pink);
}

/* ── Download ALL ── */
.dl-all-wrap div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, rgba(255,45,120,0.2), rgba(0,255,231,0.2)) !important;
    border: 1px solid var(--neon-pink) !important;
    color: var(--neon-pink) !important;
    width: 100%;
    padding: 0.7rem !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.2em !important;
    margin-top: 1rem;
}
.dl-all-wrap div[data-testid="stDownloadButton"] > button:hover {
    background: var(--neon-pink) !important;
    color: var(--dark-bg) !important;
    box-shadow: var(--glow-pink) !important;
}

/* ── Ticker ── */
.ticker {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    color: var(--text-dim);
    border-top: 1px solid var(--panel-border);
    padding-top: 1rem;
    margin-top: 2rem;
    text-align: center;
}

/* ── Status text override ── */
div[data-testid="stStatusWidget"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cyber-header">
  <div class="corner-tl"></div><div class="corner-tr"></div>
  <div class="corner-bl"></div><div class="corner-br"></div>
  <p class="cyber-title">MD<span>//</span>CONVERTER</p>
  <p class="cyber-sub">⚡ Microsoft MarkItDown · Neural Document Processor ⚡</p>
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
    f"📁 DROP FILES OR CLICK TO UPLOAD  •  supported: {ACCEPT_MAP[fmt][0]} — multiple allowed",
    type=ACCEPT_MAP[fmt],
    accept_multiple_files=True,
    key=f"uploader_{fmt}",
)

st.markdown("<br>", unsafe_allow_html=True)

# ── Convert button ────────────────────────────────────────────────────────────
convert_btn = st.button("⚡  INITIATE CONVERSION", use_container_width=True)

if convert_btn:
    if not uploaded:
        st.markdown('<div class="result-card error"><div class="result-filename">⚠ No files detected. Upload at least one file.</div></div>', unsafe_allow_html=True)
    else:
        md_tool = MarkItDown()
        results = []

        progress = st.progress(0, text="Initializing conversion matrix…")
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
        ok  = [r for r in results if r[1] is not None]
        err = [r for r in results if r[1] is None]
        total_kb = sum(len(r[1]) for r in ok) // 1024

        st.markdown(f"""
        <div class="stats-strip">
          <div class="stat-item"><span class="stat-val">{total}</span><span class="stat-lbl">Files Input</span></div>
          <div class="stat-item"><span class="stat-val" style="color:var(--neon-cyan)">{len(ok)}</span><span class="stat-lbl">Converted</span></div>
          <div class="stat-item"><span class="stat-val" style="color:var(--neon-pink)">{len(err)}</span><span class="stat-lbl">Errors</span></div>
          <div class="stat-item"><span class="stat-val">{total_kb} KB</span><span class="stat-lbl">MD Output</span></div>
        </div>
        <br>
        """, unsafe_allow_html=True)

        # ── Per-file result cards ──
        for stem, md_bytes, error in results:
            if error:
                st.markdown(f"""
                <div class="result-card error">
                  <div>
                    <div class="result-filename">✗  {stem}.md</div>
                    <div class="result-err">{error[:120]}</div>
                  </div>
                </div>""", unsafe_allow_html=True)
            else:
                chars = len(md_bytes)
                lines = md_bytes.count(b"\n")
                col_info, col_dl = st.columns([4, 1])
                with col_info:
                    st.markdown(f"""
                    <div class="result-card">
                      <div>
                        <div class="result-filename">✓  {stem}.md</div>
                        <div class="result-meta">{chars:,} chars · {lines:,} lines</div>
                      </div>
                    </div>""", unsafe_allow_html=True)
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
                f"⚡  DOWNLOAD ALL {len(ok)} FILES AS .ZIP",
                data=zip_buf.getvalue(),
                file_name="converted_markdown.zip",
                mime="application/zip",
                use_container_width=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ticker">
  POWERED BY MICROSOFT MARKITDOWN &nbsp;·&nbsp; PDF · DOCX · PPTX &nbsp;·&nbsp;
  OUTPUT FORMAT: MARKDOWN (.MD) &nbsp;·&nbsp; SYSTEM ONLINE
</div>
""", unsafe_allow_html=True)
