import streamlit as st
import io
import zipfile
from pathlib import Path
from markitdown import MarkItDown

st.set_page_config(
    page_title="MARKDOWNER | Markdown Converter",
    page_icon="☁️",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Fira+Code:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ── Exact NEBULA DRIVE tokens ── */
:root {
    --bg-grad-start: #0a0f1f;
    --bg-grad-end:   #03050b;
    --glass-bg:      rgba(12, 20, 35, 0.55);
    --glass-border:  rgba(0, 255, 255, 0.25);
    --glass-border-h:rgba(0, 255, 255, 0.55);
    --glass-shadow:  0 20px 35px -12px rgba(0,0,0,0.5), 0 0 12px rgba(0,210,255,0.2);
    --glass-shadow-h:0 20px 30px -12px rgba(0,200,255,0.25);
    --topbar-bg:     rgba(3, 7, 18, 0.7);
    --topbar-border: rgba(0, 255, 255, 0.3);
    --text:          #eef5ff;
    --text-dim:      #9dc6ff;
    --text-dimmer:   #bbddff;
    --cyan:          #0ff;
    --logo-grad:     linear-gradient(135deg, #aaffff, #4d9eff);
    --btn-primary:   linear-gradient(95deg, #0ff, #2a6eff);
    --btn-primary-fg:#01050f;
    --btn-primary-glow: 0 0 15px rgba(0,255,255,0.5);
    --code-bg:       #010a14;
    --success-bg:    rgba(0,255,200,0.1);
    --success-c:     #5effbc;
    --error-c:       #ff7780;
    --step-bg:       rgba(0, 30, 50, 0.5);
}

/* ── Force NEBULA DRIVE background everywhere ── */
html,
body,
.stApp,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stBottom"],
[data-testid="stSidebar"],
.main, section.main,
[class*="css"] {
    background: radial-gradient(circle at 20% 30%, var(--bg-grad-start), var(--bg-grad-end)) !important;
    background-color: var(--bg-grad-end) !important;
    font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif !important;
    color: var(--text) !important;
}

#MainMenu, footer, header { visibility: hidden; }

/* ── Topbar ── */
.nd-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.9rem 2rem;
    background: var(--topbar-bg);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--topbar-border);
    margin: -1rem -1rem 2rem -1rem;
}
.nd-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 600;
    font-size: 1.2rem;
    letter-spacing: -0.3px;
    background: var(--logo-grad);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.nd-badge {
    font-size: 0.7rem;
    background: rgba(0,255,255,0.1);
    padding: 2px 8px;
    border-radius: 40px;
    color: var(--cyan) !important;
}

/* ── Container ── */
.block-container {
    max-width: 1100px !important;
    margin: 0 auto !important;
    padding: 1rem 2rem 4rem !important;
}

/* ── Glass panel ── */
.glass-panel {
    background: var(--glass-bg);
    backdrop-filter: blur(14px);
    border: 1px solid var(--glass-border);
    border-radius: 2rem;
    box-shadow: var(--glass-shadow);
    padding: 2rem;
    margin-bottom: 1.5rem;
    transition: border-color 0.25s, box-shadow 0.25s;
}
.glass-panel:hover {
    border-color: var(--glass-border-h);
    box-shadow: var(--glass-shadow-h);
}

/* ── Typography ── */
h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown {
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important;
    color: var(--text) !important;
}

/* ── Section heading ── */
.nd-section-title {
    font-size: 1.8rem;
    font-weight: 800;
    background: var(--logo-grad);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-bottom: 0.3rem;
}
.nd-section-sub {
    color: var(--text-dim) !important;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}

/* ── Step label ── */
.nd-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--cyan) !important;
    font-family: 'Fira Code', monospace !important;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.nd-label::before {
    content: "▸";
    opacity: 0.6;
}

/* ── Format radio buttons ── */
div[data-testid="stRadio"] label { display: none !important; }
div[data-testid="stRadio"] > div {
    display: flex !important;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
}
div[data-testid="stRadio"] > div > label {
    display: flex !important;
    align-items: center;
    background: transparent !important;
    border: 1.2px solid var(--glass-border) !important;
    border-radius: 40px !important;
    padding: 0.5rem 1.5rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
    color: var(--cyan) !important;
    cursor: pointer;
    transition: all 0.2s;
    backdrop-filter: blur(4px);
}
div[data-testid="stRadio"] > div > label:hover {
    background: rgba(0,255,255,0.07) !important;
    border-color: var(--cyan) !important;
    box-shadow: 0 0 12px rgba(0,255,255,0.2) !important;
}
div[data-testid="stRadio"] > div > label:has(input:checked) {
    background: var(--btn-primary) !important;
    border-color: transparent !important;
    color: var(--btn-primary-fg) !important;
    box-shadow: var(--btn-primary-glow) !important;
    font-weight: 700 !important;
}
div[data-testid="stRadio"] > div > label > div:first-child { display: none !important; }

/* ── FILE UPLOADER - FULLY STREAMLIT DEFAULT, ZERO OVERRIDES ── */

/* ── Convert button ── */
div[data-testid="stButton"] > button {
    width: 100%;
    background: var(--btn-primary) !important;
    border: none !important;
    border-radius: 40px !important;
    color: var(--btn-primary-fg) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    padding: 0.85rem 2rem !important;
    box-shadow: var(--btn-primary-glow) !important;
    transition: transform 0.2s, box-shadow 0.2s;
    cursor: pointer;
}
div[data-testid="stButton"] > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 20px var(--cyan) !important;
}
div[data-testid="stButton"] > button:active {
    transform: scale(0.99);
}

/* ── Progress bar ── */
div[data-testid="stProgressBar"] > div {
    background: rgba(0, 30, 50, 0.5) !important;
    border-radius: 2rem !important;
    height: 6px !important;
    border: none !important;
}
div[data-testid="stProgressBar"] > div > div {
    background: var(--btn-primary) !important;
    border-radius: 2rem !important;
    box-shadow: 0 0 10px var(--cyan) !important;
}

/* ── Stats strip ── */
.nd-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: var(--glass-border);
    border: 1px solid var(--glass-border);
    border-radius: 1.5rem;
    overflow: hidden;
    margin: 1.5rem 0;
    backdrop-filter: blur(8px);
}
.nd-stat {
    background: var(--glass-bg);
    padding: 1.3rem 1rem;
    text-align: center;
}
.nd-stat-val {
    font-family: 'Inter', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: var(--logo-grad);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    display: block;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.nd-stat-lbl {
    font-family: 'Fira Code', monospace;
    font-size: 0.6rem;
    font-weight: 400;
    color: rgba(0,255,255,0.6) !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* ── Result cards ── */
.nd-card {
    background: rgba(8, 18, 32, 0.7);
    backdrop-filter: blur(8px);
    border: 1px solid var(--glass-border);
    border-radius: 1.5rem;
    padding: 1rem 1.3rem;
    margin: 0.5rem 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.nd-card:hover {
    border-color: var(--glass-border-h);
    box-shadow: 0 0 15px rgba(0,255,255,0.15);
}
.nd-card.nd-ok   { border-left: 4px solid var(--success-c); }
.nd-card.nd-error { border-left: 4px solid var(--error-c); }
.nd-filename {
    font-family: 'Fira Code', monospace;
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--text) !important;
    word-break: break-word;
}
.nd-card.nd-ok .nd-filename   { color: var(--success-c) !important; }
.nd-card.nd-error .nd-filename { color: var(--error-c) !important; }
.nd-meta {
    font-family: 'Fira Code', monospace;
    font-size: 0.7rem;
    color: rgba(0,255,255,0.55) !important;
    margin-top: 0.2rem;
}
.nd-errmsg {
    font-family: 'Fira Code', monospace;
    font-size: 0.72rem;
    color: var(--error-c) !important;
    margin-top: 0.2rem;
}

/* ── Download individual button ── */
div[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    border: 1.2px solid var(--cyan) !important;
    border-radius: 40px !important;
    color: var(--cyan) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    padding: 6px 16px !important;
    transition: all 0.2s;
    white-space: nowrap;
    backdrop-filter: blur(4px);
    cursor: pointer;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: rgba(0,255,255,0.1) !important;
    box-shadow: 0 0 12px rgba(0,255,255,0.4) !important;
    color: #fff !important;
}

/* ── Download all ZIP ── */
.dl-all-wrap div[data-testid="stDownloadButton"] > button {
    background: var(--btn-primary) !important;
    border: none !important;
    color: var(--btn-primary-fg) !important;
    width: 100%;
    padding: 0.8rem 2rem !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    border-radius: 40px !important;
    box-shadow: var(--btn-primary-glow) !important;
}
.dl-all-wrap div[data-testid="stDownloadButton"] > button:hover {
    transform: scale(1.01);
    box-shadow: 0 0 20px var(--cyan) !important;
}

/* ── Success box ── */
.nd-success-pulse {
    background: var(--success-bg);
    border: 1px solid var(--cyan);
    border-radius: 1rem;
    padding: 1rem 1.2rem;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 1rem;
    font-size: 0.85rem;
}

/* ── Footer ── */
.nd-footer {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid var(--glass-border);
    margin-top: 3rem;
}
.nd-footer p {
    font-family: 'Fira Code', monospace !important;
    font-size: 0.65rem !important;
    color: rgba(0,255,255,0.35) !important;
    letter-spacing: 0.1em;
}

/* ── Custom scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #10141e; }
::-webkit-scrollbar-thumb { background: rgba(0,255,255,0.2); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,255,255,0.4); }

/* ── Text selection ── */
::selection { background: rgba(0,255,255,0.2); color: #fff; }

/* ── stMarkdown text ── */
.stMarkdown p, .stMarkdown li, .stMarkdown span {
    color: var(--text-dimmer) !important;
    font-size: 0.9rem;
    line-height: 1.6;
}

/* ── Status widget hide ── */
div[data-testid="stStatusWidget"] { display: none !important; }

/* ── Column alignment fix for result rows ── */
[data-testid="stColumn"] { align-items: center !important; }
</style>
""", unsafe_allow_html=True)

# ── Topbar ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nd-topbar">
  <div class="nd-logo">
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#0ff" stroke-width="1.5"
         style="filter:drop-shadow(0 0 5px cyan)">
      <path d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"/>
      <path d="M12 12v5m0 0l-2-2m2 2l2-2"/>
    </svg>
    MARKDOWNER
    <span class="nd-badge">Markdown Converter</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Hero section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="glass-panel">
  <div class="nd-section-title">✦ MARKDOWNER</div>
  <p class="nd-section-sub">AI-powered document conversion — PDF, PPTX and DOCX to Markdown using Microsoft MarkItDown</p>
</div>
""", unsafe_allow_html=True)

# ── Format selector ───────────────────────────────────────────────────────────
st.markdown('<div class="nd-label">Select input format</div>', unsafe_allow_html=True)
fmt = st.radio("format", ["PDF", "PPTX", "DOCX"], horizontal=True, label_visibility="collapsed")
ACCEPT_MAP = {"PDF": [".pdf"], "PPTX": [".pptx"], "DOCX": [".docx"]}

# ── File uploader - NO CUSTOM CSS, PURE STREAMLIT DEFAULT ────────────────────
uploaded = st.file_uploader(
    f"Upload {fmt}",
    type=ACCEPT_MAP[fmt],
    accept_multiple_files=True,
    key=f"uploader_{fmt}",
    label_visibility="collapsed",
)

st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

# ── Convert button ────────────────────────────────────────────────────────────
convert_btn = st.button("⚡  Convert to Markdown", use_container_width=True)

if convert_btn:
    if not uploaded:
        st.markdown("""
        <div class="nd-card nd-error">
          <div>
            <div class="nd-filename">⚠ No files detected</div>
            <div class="nd-errmsg">Upload at least one file to proceed.</div>
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        md_tool = MarkItDown()
        results = []
        progress = st.progress(0, text="Initializing…")
        total = len(uploaded)

        MAX_BYTES = 10 * 1024 * 1024  # 10 MB

        for i, f in enumerate(uploaded):
            stem = Path(f.name).stem
            progress.progress(i / total, text=f"Converting {i+1} of {total} — {f.name}")
            try:
                raw = f.read()
                if len(raw) > MAX_BYTES:
                    size_mb = len(raw) / 1024 / 1024
                    results.append((stem, None, f"File too large ({size_mb:.1f} MB) — 10 MB maximum per file."))
                    continue
                result = md_tool.convert_stream(
                    io.BytesIO(raw),
                    file_extension=Path(f.name).suffix.lower(),
                )
                results.append((stem, result.text_content.encode("utf-8"), None))
            except Exception as e:
                results.append((stem, None, str(e)))

        progress.progress(1.0, text="Conversion complete.")

        ok  = [r for r in results if r[1] is not None]
        err = [r for r in results if r[1] is None]
        total_kb = sum(len(r[1]) for r in ok) // 1024

        # Stats strip
        st.markdown(f"""
        <div class="nd-stats">
          <div class="nd-stat">
            <span class="nd-stat-val">{total}</span>
            <span class="nd-stat-lbl">Input</span>
          </div>
          <div class="nd-stat">
            <span class="nd-stat-val">{len(ok)}</span>
            <span class="nd-stat-lbl">Converted</span>
          </div>
          <div class="nd-stat">
            <span class="nd-stat-val">{len(err)}</span>
            <span class="nd-stat-lbl">Errors</span>
          </div>
          <div class="nd-stat">
            <span class="nd-stat-val">{total_kb}</span>
            <span class="nd-stat-lbl">KB Output</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="nd-label" style="margin-top:1rem">Results</div>', unsafe_allow_html=True)

        for stem, md_bytes, error in results:
            if error:
                st.markdown(f"""
                <div class="nd-card nd-error">
                  <div>
                    <div class="nd-filename">✗  {stem}.md</div>
                    <div class="nd-errmsg">{error[:140]}</div>
                  </div>
                </div>""", unsafe_allow_html=True)
            else:
                chars = len(md_bytes)
                lines = md_bytes.count(b"\n")
                col_info, col_dl = st.columns([5, 1])
                with col_info:
                    st.markdown(f"""
                    <div class="nd-card nd-ok">
                      <div>
                        <div class="nd-filename">✓  {stem}.md</div>
                        <div class="nd-meta">{chars:,} chars · {lines:,} lines</div>
                      </div>
                    </div>""", unsafe_allow_html=True)
                with col_dl:
                    st.download_button(
                        "↓ Save",
                        data=md_bytes,
                        file_name=f"{stem}.md",
                        mime="text/markdown",
                        key=f"dl_{stem}",
                        use_container_width=True,
                    )

        if len(ok) > 0:
            share_name = f"{len(ok)} file{'s' if len(ok)>1 else ''}"
            st.markdown(f"""
            <div class="nd-success-pulse">
              <span>☁</span>
              <span><strong>{share_name} converted</strong><br>
              Your Markdown files are ready — End-to-End processed by Microsoft MarkItDown</span>
            </div>""", unsafe_allow_html=True)

        if len(ok) > 1:
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
                for stem, md_bytes, _ in ok:
                    zf.writestr(f"{stem}.md", md_bytes)
            st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
            st.markdown('<div class="dl-all-wrap">', unsafe_allow_html=True)
            st.download_button(
                f"⬇  Download all {len(ok)} files as .zip",
                data=zip_buf.getvalue(),
                file_name="converted_markdown.zip",
                mime="application/zip",
                use_container_width=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nd-footer">
  <p>MARKDOWNER · MARKDOWN CONVERTER · POWERED BY MICROSOFT MARKITDOWN · PDF · DOCX · PPTX</p>
</div>
""", unsafe_allow_html=True)