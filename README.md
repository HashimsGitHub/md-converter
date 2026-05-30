<div align="center">

# ✦ MARKDOWNER

### Markdown Converter · Powered by Microsoft MarkItDown

[![Live App](https://img.shields.io/badge/Live%20App-markdowner.streamlit.app-00ffe7?style=for-the-badge&logo=streamlit&logoColor=white)](https://markdowner.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10+-4d9eff?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Framework-ff007f?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![MarkItDown](https://img.shields.io/badge/Microsoft-MarkItDown-0078d4?style=for-the-badge&logo=microsoft&logoColor=white)](https://github.com/microsoft/markitdown)

</div>

---

## 🌐 Live Demo

**[https://markdowner.streamlit.app/](https://markdowner.streamlit.app/)**

<!-- Screenshot -->

---

## 📖 Overview

**Markdowner** is a sleek, browser-based document converter that transforms **PDF**, **PPTX**, and **DOCX** files into clean **Markdown** (`.md`) using Microsoft's open-source [MarkItDown](https://github.com/microsoft/markitdown) library. Built with a futuristic glassmorphism UI inspired by the Nebula Drive design system.

Upload multiple files at once, convert them in batch, and download individually or as a single `.zip` archive — no sign-in required.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **Multi-format support** | Convert PDF, PPTX, and DOCX files |
| 📦 **Batch processing** | Upload and convert multiple files simultaneously |
| ⬇️ **Flexible download** | Save files individually or all as a `.zip` |
| 🛡️ **10 MB file limit** | Per-file size cap to keep conversions fast |
| 🎨 **Nebula Drive UI** | Glassmorphism dark theme with neon cyan accents |
| ⚡ **Zero config** | No login, no API key — just upload and convert |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher

### Installation

```bash
# Clone the repository
git clone https://github.com/HashimsGitHub/md-converter.git
cd md-converter

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📦 Dependencies

```txt
streamlit
markitdown[pdf,docx,pptx]
```

---

## 🗂️ Supported Formats

| Input Format | Extension | Output |
|---|---|---|
| PDF Document | `.pdf` | `.md` |
| PowerPoint Presentation | `.pptx` | `.md` |
| Word Document | `.docx` | `.md` |

> **File size limit:** 10 MB per file

---

## 🏗️ Architecture

```
User Browser
     │
     ▼
Markdowner (Streamlit App)
     │
     ▼
Microsoft MarkItDown Engine
     │
     ▼
Markdown Output (.md files)
```

---

## 📁 Project Structure

```
md-converter/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit + Custom CSS (Glassmorphism) |
| Conversion Engine | Microsoft MarkItDown |
| Fonts | Inter · Fira Code |
| Hosting | Streamlit Community Cloud |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Built with ☁️ · Deployed on Streamlit Cloud

</div>
