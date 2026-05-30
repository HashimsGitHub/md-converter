import streamlit as st
import io
import zipfile
from pathlib import Path
from markitdown import MarkItDown

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MD//CONVERTER",
    page_icon="⚡",
    layout="centered",
)

# ── Cyberpunk CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

:root {
    --neon-cyan:    #00ffe7;
    --neon-pink:    #ff2d78;
    --neon-yellow:  #f5e642;
    --dark-bg:      #080b14;
    --panel-bg:     #0d1526;
    --panel-border: #1a2a4a;
    --text-main:    #c8d8f0;
    --text-dim:     #4a6080;
    --glow-cyan:    0 0 8px #00ffe7, 0 0 20px #00ffe780;
    --glow-pink:    0 0 8px #ff2d78, 0 0 20px #ff2d7880;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background-color: var(--dark-bg) !important;
    color: var(--text-main) !important;
}

/* ── Scanlines overlay ── */
body::before {
    content: "";
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,255,231,0.025) 2px,
        rgba(0,255,231,0.025) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 1.5rem !important; max-width: 820px !important; }

/* ── Header ── */
.cyber-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    position: relative;
}
.cyber-title {
    font-family: 'Orbitron', monospace;
    font-size: 3rem;
    font-weight: 900;
    letter-spacing: 0.15em;
    color: var(--neon-cyan);
    text-shadow: var(--glow-cyan);
    margin: 0;
    line-height: 1;
}
.cyber-title span { color: var(--neon-pink); text-shadow: var(--glow-pink); }
.cyber-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: var(--text-dim);
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-top: 0.5rem;
}
.corner-tl, .corner-tr, .corner-bl, .corner-br {
    position: absolute;
    width: 18px; height: 18px;
    border-color: var(--neon-cyan);
    border-style: solid;
    opacity: 0.6;
}
.corner-tl { top:0; left:0;  border-width: 2px 0 0 2px; }
.corner-tr { top:0; right:0; border-width: 2px 2px 0 0; }
.corner-bl { bottom:0; left:0;  border-width: 0 0 2px 2px; }
.corner-br { bottom:0; right:0; border-width: 0 2px 2px 0; }

/* ── Divider ── */
.cyber-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), var(--neon-pink), transparent);
    margin: 1rem 0 2rem;
    opacity: 0.5;
}

/* ── Format selector label ── */
.format-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    color: var(--neon-cyan);
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

/* ── Streamlit radio / selectbox tweaks ── */
div[data-testid="stRadio"] label,
div[data-testid="stSelectbox"] label { display: none; }

div[data-testid="stRadio"] > div {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
}
div[data-testid="stRadio"] > div > label {
    display: flex !important;
    align-items: center;
    gap: 0.4rem;
    font-family: 'Orbitron', monospace;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: var(--text-dim) !important;
    background: var(--panel-bg);
    border: 1px solid var(--panel-border);
    padding: 0.55rem 1.1rem;
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
}
div[data-testid="stRadio"] > div > label:hover {
    color: var(--neon-cyan) !important;
    border-color: var(--neon-cyan);
    box-shadow: inset 0 0 12px rgba(0,255,231,0.07), var(--glow-cyan);
}
div[data-testid="stRadio"] > div > label[data-checked="true"],
div[data-testid="stRadio"] > div > label:has(input:checked) {
    color: var(--neon-cyan) !important;
    border-color: var(--neon-cyan) !important;
    box-shadow: inset 0 0 16px rgba(0,255,231,0.1), var(--glow-cyan);
}

/* ── File uploader ── */
div[data-testid="stFileUploader"] {
    border: 1px dashed var(--neon-pink) !important;
    background: var(--panel-bg) !important;
    border-radius: 0 !important;
    padding: 1.5rem !important;
    position: relative;
    transition: border-color 0.2s, box-shadow 0.2s;
}
div[data-testid="stFileUploader"]:hover {
    border-color: var(--neon-cyan) !important;
    box-shadow: var(--glow-cyan);
}
div[data-testid="stFileUploader"] label {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.8rem !important;
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
    box-shadow: var(--glow-pink);
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
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
    overflow: hidden;
}
div[data-testid="stButton"] > button:hover {
    background: var(--neon-cyan) !important;
    color: var(--dark-bg) !important;
    box-shadow: var(--glow-cyan);
}

/* ── Progress / status ── */
.stProgress > div > div { background: var(--neon-cyan) !important; }
div[data-testid="stStatusWidget"] { display: none; }

/* ── Result cards ── */
.result-card {
    background: var(--panel-bg);
    border: 1px solid var(--panel-border);
    border-left: 3px solid var(--neon-cyan);
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}
.result-card.error {
    border-left-color: var(--neon-pink);
}
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

/* ── Download all button ── */
div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, var(--neon-pink)22, var(--neon-cyan)22) !important;
    border: 1px solid var(--neon-pink) !important;
    color: var(--neon-pink) !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.2em !important;
    border-radius: 0 !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: var(--neon-pink) !important;
    color: var(--dark-bg) !important;
    box-shadow: var(--glow-pink);
}

/* ── Stats strip ── */
.stats-strip {
    display: flex;
    gap: 1.5rem;
    background: var(--panel-bg);
    border: 1px solid var(--panel-border);
    padding: 0.8rem 1.2rem;
    margin-top: 1.5rem;
    flex-wrap: wrap;
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

/* ── Ticker line ── */
.ticker {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    color: var(--text-dim);
    letter-spacing: 0.1em;
    border-top: 1px solid var(--panel-border);
    padding-top: 1rem;
    margin-top: 2rem;
    text-align: center;
}
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
st.markdown('<p class="format-label">▸ Select Input Format</p>', unsafe_allow_html=True)

fmt = st.radio(
    "format",
    ["PDF", "PPTX", "DOCX"],
    horizontal=True,
    label_visibility="collapsed",
)

ACCEPT_MAP = {
    "PDF":  [".pdf"],
    "PPTX": [".pptx"],
    "DOCX": [".docx"],
}
TYPE_MAP = {
    "PDF":  "application/pdf",
    "PPTX": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "DOCX": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

st.markdown("<br>", unsafe_allow_html=True)

# ── File uploader ─────────────────────────────────────────────────────────────
uploaded = st.file_uploader(
    f"Drop {fmt} files here — multiple allowed",
    type=ACCEPT_MAP[fmt],
    accept_multiple_files=True,
    key=f"uploader_{fmt}",
)

st.markdown("<br>", unsafe_allow_html=True)

# ── Convert ───────────────────────────────────────────────────────────────────
convert_btn = st.button("⚡  INITIATE CONVERSION", use_container_width=True)

if convert_btn:
    if not uploaded:
        st.error("⚠  No files detected. Upload at least one file to proceed.")
    else:
        md_tool = MarkItDown()
        results = []  # list of (stem, md_bytes | None, error_msg)

        progress = st.progress(0, text="Initializing conversion matrix…")
        total = len(uploaded)

        for i, f in enumerate(uploaded):
            stem = Path(f.name).stem
            progress.progress((i) / total, text=f"[{i+1}/{total}] Converting: {f.name}")
            try:
                raw = f.read()
                result = md_tool.convert_stream(
                    io.BytesIO(raw),
                    file_extension=Path(f.name).suffix.lower(),
                )
                md_text = result.text_content
                results.append((stem, md_text.encode("utf-8"), None))
            except Exception as e:
                results.append((stem, None, str(e)))

        progress.progress(1.0, text="Conversion complete.")

        # ── Stats strip ──
        ok_count  = sum(1 for _, b, _ in results if b is not None)
        err_count = total - ok_count
        total_kb  = sum(len(b) for _, b, _ in results if b) // 1024

        st.markdown(f"""
        <div class="stats-strip">
          <div class="stat-item">
            <span class="stat-val">{total}</span>
            <span class="stat-lbl">Files Input</span>
          </div>
          <div class="stat-item">
            <span class="stat-val" style="color:var(--neon-cyan)">{ok_count}</span>
            <span class="stat-lbl">Converted</span>
          </div>
          <div class="stat-item">
            <span class="stat-val" style="color:var(--neon-pink)">{err_count}</span>
            <span class="stat-lbl">Errors</span>
          </div>
          <div class="stat-item">
            <span class="stat-val">{total_kb} KB</span>
            <span class="stat-lbl">MD Output</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Per-file results ──
        for stem, md_bytes, err in results:
            if err:
                st.markdown(f"""
                <div class="result-card error">
                  <div>
                    <div class="result-filename">✗  {stem}.md</div>
                    <div class="result-err">{err[:120]}</div>
                  </div>
                </div>""", unsafe_allow_html=True)
            else:
                col_info, col_dl = st.columns([3, 1])
                with col_info:
                    chars = len(md_bytes)
                    lines = md_bytes.count(b"\n")
                    st.markdown(f"""
                    <div class="result-card">
                      <div>
                        <div class="result-filename">✓  {stem}.md</div>
                        <div class="result-meta">{chars:,} chars · {lines:,} lines</div>
                      </div>
                    </div>""", unsafe_allow_html=True)
                with col_dl:
                    st.markdown("<div style='margin-top:0.5rem'>", unsafe_allow_html=True)
                    st.download_button(
                        "↓ SAVE",
                        data=md_bytes,
                        file_name=f"{stem}.md",
                        mime="text/markdown",
                        key=f"dl_{stem}",
                    )
                    st.markdown("</div>", unsafe_allow_html=True)

        # ── Download all as ZIP ──
        if ok_count > 1:
            st.markdown("<br>", unsafe_allow_html=True)
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
                for stem, md_bytes, _ in results:
                    if md_bytes:
                        zf.writestr(f"{stem}.md", md_bytes)
            st.download_button(
                f"⚡  DOWNLOAD ALL {ok_count} FILES AS .ZIP",
                data=zip_buf.getvalue(),
                file_name="converted_markdown.zip",
                mime="application/zip",
                use_container_width=True,
            )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ticker">
  POWERED BY MICROSOFT MARKITDOWN &nbsp;·&nbsp; PDF · DOCX · PPTX &nbsp;·&nbsp;
  OUTPUT FORMAT: MARKDOWN (.MD) &nbsp;·&nbsp; SYSTEM ONLINE
</div>
""", unsafe_allow_html=True)
