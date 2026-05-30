import streamlit as st
import io
import zipfile
from pathlib import Path
from markitdown import MarkItDown

st.set_page_config(
    page_title="MD//CONVERTER",
    page_icon="⚡",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Mono:wght@400;700&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg:           #000000;
    --surface:      #0d0d0d;
    --surface-2:    #141414;
    --surface-3:    #1a1a1a;
    --border:       rgba(255,255,255,0.08);
    --border-hover: rgba(255,255,255,0.18);
    --text:         #ffffff;
    --text-secondary: rgba(255,255,255,0.55);
    --text-tertiary:  rgba(255,255,255,0.35);
    --green:        #238636;
    --green-hover:  #2ea043;
    --green-light:  #3fb950;
    --red:          #f85149;
    --yellow:       #e3b341;
    --blue:         #58a6ff;
    --purple:       #bc8cff;
}

/* ── Force black everywhere ── */
html, body,
.stApp, .stApp > header, .stApp > div,
.main, section.main,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stBottom"],
[data-testid="stSidebar"],
[class*="css"] {
    background: #000000 !important;
    background-color: #000000 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text) !important;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    max-width: 860px !important;
    margin: 0 auto !important;
    padding: 3rem 2rem 4rem !important;
}

/* ── Typography ── */
h1, h2, h3, h4, h5, h6, p, span, div, label,
.stMarkdown, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text) !important;
}

/* ── Header ── */
.nd-header {
    text-align: center;
    padding: 2.5rem 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
}

.nd-wordmark {
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: var(--text-secondary) !important;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}

.nd-wordmark::before, .nd-wordmark::after {
    content: "";
    display: inline-block;
    width: 24px;
    height: 1px;
    background: var(--border-hover);
}

.nd-title {
    font-family: 'Inter', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #ffffff !important;
    line-height: 1.1;
    margin-bottom: 0.6rem;
}

.nd-title .slash {
    color: var(--text-tertiary) !important;
    font-weight: 300;
}

.nd-sub {
    font-size: 0.85rem;
    font-weight: 400;
    color: var(--text-secondary) !important;
    letter-spacing: 0.01em;
}

/* ── Section label ── */
.nd-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-secondary) !important;
    margin-bottom: 0.75rem;
    font-family: 'Space Mono', monospace !important;
}

/* ── Format radio ── */
div[data-testid="stRadio"] label { display: none !important; }
div[data-testid="stRadio"] > div {
    display: flex !important;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}
div[data-testid="stRadio"] > div > label {
    display: flex !important;
    align-items: center;
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    padding: 0.55rem 1.4rem !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    color: var(--text-secondary) !important;
    cursor: pointer;
    transition: all 0.15s ease;
}
div[data-testid="stRadio"] > div > label:hover {
    background: var(--surface-2) !important;
    border-color: var(--border-hover) !important;
    color: var(--text) !important;
}
div[data-testid="stRadio"] > div > label:has(input:checked) {
    background: var(--green) !important;
    border-color: var(--green) !important;
    color: #ffffff !important;
}
div[data-testid="stRadio"] > div > label > div:first-child { display: none !important; }

/* ── File uploader — nuke every layer ── */
div[data-testid="stFileUploader"],
div[data-testid="stFileUploader"] > div,
div[data-testid="stFileUploader"] section,
div[data-testid="stFileUploader"] section > div,
div[data-testid="stFileUploaderDropzone"],
div[data-testid="stFileUploaderDropzoneInstructions"],
div[data-testid="stFileUploaderDropzoneInstructions"] > div {
    background: var(--surface) !important;
    background-color: var(--surface) !important;
}
div[data-testid="stFileUploader"] {
    border: 1px dashed rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
    transition: border-color 0.15s, background 0.15s;
}
div[data-testid="stFileUploader"]:hover {
    border-color: rgba(255,255,255,0.4) !important;
    background: var(--surface-2) !important;
}
div[data-testid="stFileUploader"] label,
div[data-testid="stFileUploader"] span,
div[data-testid="stFileUploader"] p,
div[data-testid="stFileUploaderDropzoneInstructions"] span,
div[data-testid="stFileUploaderDropzoneInstructions"] p {
    font-family: 'Inter', sans-serif !important;
    color: rgba(255,255,255,0.6) !important;
    background: transparent !important;
}
div[data-testid="stFileUploader"] small,
div[data-testid="stFileUploaderDropzoneInstructions"] small {
    color: rgba(255,255,255,0.3) !important;
    font-size: 0.72rem !important;
}
div[data-testid="stFileUploader"] button {
    background: var(--green) !important;
    border: none !important;
    border-radius: 6px !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    padding: 0.45rem 1.1rem !important;
    transition: background 0.15s;
    cursor: pointer;
}
div[data-testid="stFileUploader"] button:hover {
    background: var(--green-hover) !important;
}

/* ── Uploaded file badges ── */
[data-testid="stFileUploaderFile"],
[data-testid="stFileUploaderFile"] > div {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
}
[data-testid="stFileUploaderFileName"] {
    color: var(--text) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
}
[data-testid="stFileUploaderFileData"] {
    color: var(--text-secondary) !important;
    font-size: 0.7rem !important;
}
[data-testid="stFileUploaderDeleteBtn"] button {
    color: var(--text-secondary) !important;
    background: transparent !important;
    border: none !important;
}
[data-testid="stFileUploaderDeleteBtn"] button:hover {
    color: var(--red) !important;
}

/* ── Convert button ── */
div[data-testid="stButton"] > button {
    width: 100%;
    background: var(--green) !important;
    border: none !important;
    border-radius: 6px !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    padding: 0.75rem 1.5rem !important;
    transition: background 0.15s, transform 0.1s;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}
div[data-testid="stButton"] > button:hover {
    background: var(--green-hover) !important;
    transform: translateY(-1px);
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0);
}

/* ── Progress bar ── */
div[data-testid="stProgressBar"] > div {
    background: var(--surface-2) !important;
    border-radius: 4px !important;
    height: 4px !important;
    border: none !important;
}
div[data-testid="stProgressBar"] > div > div {
    background: var(--green-light) !important;
    border-radius: 4px !important;
    box-shadow: none !important;
}
/* Progress label text */
[data-testid="stProgressBar"] ~ div p,
[data-testid="stProgressBar"] + div p {
    color: var(--text-secondary) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
}

/* ── Stats strip ── */
.nd-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    margin: 1.5rem 0;
}
.nd-stat {
    background: var(--surface);
    padding: 1.2rem 1rem;
    text-align: center;
}
.nd-stat-val {
    font-family: 'Inter', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #ffffff;
    display: block;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.nd-stat-lbl {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    font-weight: 400;
    color: var(--text-secondary);
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── Result cards ── */
.nd-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.9rem 1.1rem;
    margin: 0.4rem 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    transition: border-color 0.15s;
}
.nd-card:hover { border-color: var(--border-hover); }
.nd-card.nd-error { border-left: 3px solid var(--red); }
.nd-card.nd-ok   { border-left: 3px solid var(--green-light); }
.nd-filename {
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
    font-weight: 400;
    color: #ffffff;
}
.nd-card.nd-error .nd-filename { color: var(--red); }
.nd-meta {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    color: var(--text-secondary);
    margin-top: 0.2rem;
}
.nd-errmsg {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--red);
    margin-top: 0.2rem;
}

/* ── Download buttons ── */
div[data-testid="stDownloadButton"] > button {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    padding: 0.4rem 0.9rem !important;
    transition: all 0.15s;
    white-space: nowrap;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: var(--surface-3) !important;
    border-color: var(--border-hover) !important;
    color: #ffffff !important;
}

/* ── Download all ZIP ── */
.dl-all-wrap div[data-testid="stDownloadButton"] > button {
    background: var(--green) !important;
    border: none !important;
    color: #ffffff !important;
    width: 100%;
    padding: 0.7rem !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
}
.dl-all-wrap div[data-testid="stDownloadButton"] > button:hover {
    background: var(--green-hover) !important;
}

/* ── Divider ── */
.nd-divider {
    height: 1px;
    background: var(--border);
    margin: 2rem 0;
}

/* ── Footer ── */
.nd-footer {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
}
.nd-footer p {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.65rem !important;
    color: var(--text-tertiary) !important;
    letter-spacing: 0.08em;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #000; }
::-webkit-scrollbar-thumb { background: var(--surface-3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }

/* ── Text selection ── */
::selection { background: rgba(46,160,67,0.35); color: #fff; }

/* ── stMarkdown text ── */
.stMarkdown p, .stMarkdown li, .stMarkdown span {
    color: var(--text-secondary) !important;
    font-size: 0.9rem;
    line-height: 1.6;
}

/* ── Status widget hide ── */
div[data-testid="stStatusWidget"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nd-header">
  <div class="nd-wordmark">NEBULA DRIVE · NEURAL DOCUMENT PROCESSOR</div>
  <div class="nd-title">MD<span class="slash"> // </span>CONVERTER</div>
  <div class="nd-sub">Convert PDF, PPTX and DOCX files to Markdown — powered by Microsoft MarkItDown</div>
</div>
""", unsafe_allow_html=True)

# ── Format selector ───────────────────────────────────────────────────────────
st.markdown('<div class="nd-label">Select input format</div>', unsafe_allow_html=True)

fmt = st.radio("format", ["PDF", "PPTX", "DOCX"], horizontal=True, label_visibility="collapsed")

ACCEPT_MAP = {"PDF": [".pdf"], "PPTX": [".pptx"], "DOCX": [".docx"]}

# ── File uploader ─────────────────────────────────────────────────────────────
st.markdown('<div class="nd-label" style="margin-top:1.5rem">Upload files</div>', unsafe_allow_html=True)

uploaded = st.file_uploader(
    f"Drop {fmt} files here or click to browse — multiple files supported",
    type=ACCEPT_MAP[fmt],
    accept_multiple_files=True,
    key=f"uploader_{fmt}",
)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ── Convert button ────────────────────────────────────────────────────────────
convert_btn = st.button("⚡  Convert to Markdown", use_container_width=True)

if convert_btn:
    if not uploaded:
        st.markdown("""
        <div class="nd-card nd-error">
          <div>
            <div class="nd-filename">No files detected</div>
            <div class="nd-errmsg">Upload at least one file to proceed.</div>
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        md_tool = MarkItDown()
        results = []

        progress = st.progress(0, text="Initializing…")
        total = len(uploaded)

        for i, f in enumerate(uploaded):
            stem = Path(f.name).stem
            progress.progress(i / total, text=f"Converting {i+1} of {total} — {f.name}")
            try:
                raw = f.read()
                result = md_tool.convert_stream(
                    io.BytesIO(raw),
                    file_extension=Path(f.name).suffix.lower(),
                )
                results.append((stem, result.text_content.encode("utf-8"), None))
            except Exception as e:
                results.append((stem, None, str(e)))

        progress.progress(1.0, text="Done.")

        # ── Stats ──
        ok  = [r for r in results if r[1] is not None]
        err = [r for r in results if r[1] is None]
        total_kb = sum(len(r[1]) for r in ok) // 1024

        ok_color  = "#3fb950" if len(ok) > 0 else "#ffffff"
        err_color = "#f85149" if len(err) > 0 else "#ffffff"

        st.markdown(f"""
        <div class="nd-stats">
          <div class="nd-stat">
            <span class="nd-stat-val">{total}</span>
            <span class="nd-stat-lbl">Input</span>
          </div>
          <div class="nd-stat">
            <span class="nd-stat-val" style="color:{ok_color}">{len(ok)}</span>
            <span class="nd-stat-lbl">Converted</span>
          </div>
          <div class="nd-stat">
            <span class="nd-stat-val" style="color:{err_color}">{len(err)}</span>
            <span class="nd-stat-lbl">Errors</span>
          </div>
          <div class="nd-stat">
            <span class="nd-stat-val">{total_kb}</span>
            <span class="nd-stat-lbl">KB Output</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Per-file cards ──
        st.markdown('<div class="nd-label">Results</div>', unsafe_allow_html=True)

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

        # ── Download all as ZIP ──
        if len(ok) > 1:
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
                for stem, md_bytes, _ in ok:
                    zf.writestr(f"{stem}.md", md_bytes)
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
  <p>POWERED BY MICROSOFT MARKITDOWN &nbsp;·&nbsp; PDF · DOCX · PPTX &nbsp;·&nbsp; OUTPUT: MARKDOWN (.MD)</p>
</div>
""", unsafe_allow_html=True)
