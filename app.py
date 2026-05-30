import streamlit as st
import io
import zipfile
from pathlib import Path
from markitdown import MarkItDown

# --- Page Config ---
st.set_page_config(
    page_title="Markdowner | Markdown Converter",
    page_icon="📝",
    layout="wide"
)

# --- Header ---
st.markdown("""
    <div style="display:flex; align-items:center; gap:15px; background-color:#0078D4; padding:15px; border-radius:10px; color:white;">
        <span style="font-size:40px;">📝</span>
        <div>
            <h1 style="margin:0;">MARKDOWNER</h1>
            <p style="margin:0; opacity:0.85; font-size:14px;">Markdown Converter — Powered by Microsoft MarkItDown</p>
        </div>
    </div>
    <p style="margin-top:10px; font-size:16px; color:#333;">
        Upload PDF, PPTX or DOCX files and convert them to clean Markdown (.md) files 📄
    </p>
""", unsafe_allow_html=True)

# --- Format selector ---
st.markdown("### 📂 Select Input Format")
fmt = st.radio("Format", ["PDF", "PPTX", "DOCX"], horizontal=True)

ACCEPT_MAP = {"PDF": [".pdf"], "PPTX": [".pptx"], "DOCX": [".docx"]}
MAX_BYTES = 10 * 1024 * 1024  # 10 MB

# --- File uploader --- (same bare pattern as NSG app — no label_visibility, no CSS)
uploaded = st.file_uploader(
    f"📂 Upload {fmt} files (max 10MB per file, multiple files supported)",
    type=ACCEPT_MAP[fmt],
    accept_multiple_files=True,
    key=f"uploader_{fmt}",
)

# --- Convert button ---
if st.button("⚡ Convert to Markdown", use_container_width=True):
    if not uploaded:
        st.warning("⚠️ No files uploaded. Please select at least one file.")
    else:
        md_tool = MarkItDown()
        results = []
        total = len(uploaded)
        progress = st.progress(0, text="Starting conversion…")

        for i, f in enumerate(uploaded):
            stem = Path(f.name).stem
            progress.progress(i / total, text=f"Converting {i+1}/{total} — {f.name}")
            try:
                raw = f.read()
                if len(raw) > MAX_BYTES:
                    size_mb = len(raw) / 1024 / 1024
                    results.append((stem, None, f"File too large ({size_mb:.1f} MB) — 10 MB max."))
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

        # --- Stats ---
        st.markdown("---")
        st.markdown("### 📊 Conversion Summary")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Files Input",  total)
        col2.metric("Converted",    len(ok))
        col3.metric("Errors",       len(err))
        col4.metric("KB Output",    total_kb)

        # --- Results ---
        st.markdown("### 📄 Results")

        for stem, md_bytes, error in results:
            if error:
                st.error(f"✗ **{stem}.md** — {error}")
            else:
                chars = len(md_bytes)
                lines = md_bytes.count(b"\n")
                col_info, col_dl = st.columns([5, 1])
                with col_info:
                    st.success(f"✓ **{stem}.md** — {chars:,} chars · {lines:,} lines")
                with col_dl:
                    st.download_button(
                        label="⬇ Save",
                        data=md_bytes,
                        file_name=f"{stem}.md",
                        mime="text/markdown",
                        key=f"dl_{stem}",
                        use_container_width=True,
                    )

        # --- Download all as ZIP ---
        if len(ok) > 1:
            st.markdown("---")
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
                for stem, md_bytes, _ in ok:
                    zf.writestr(f"{stem}.md", md_bytes)
            st.download_button(
                label=f"⬇ Download all {len(ok)} files as .zip",
                data=zip_buf.getvalue(),
                file_name="converted_markdown.zip",
                mime="application/zip",
                use_container_width=True,
            )

else:
    st.info("👆 Select a format, upload your files, then click Convert.")

# --- Footer ---
st.markdown("""
    <hr style="margin-top:40px;">
    <div style="text-align:center; color:gray; font-size:14px;">
        Built with ❤️ using Streamlit & Microsoft MarkItDown<br>
        © 2025 Hashim Hilal — Cloud Architect
    </div>
""", unsafe_allow_html=True)
