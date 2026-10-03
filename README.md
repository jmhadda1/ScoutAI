# 🔍 Scout AI

> **AI-powered purchase analysis for Facebook Marketplace.**

Scout AI helps buyers make smarter decisions when purchasing used electronics by analyzing Marketplace screenshots and generating a Purchase Confidence Score with AI-powered insights.

---

# Demo

1. Upload a Facebook Marketplace screenshot.
2. Scout AI extracts listing information using OCR.
3. A local AI model interprets the listing.
4. Scout Engine evaluates the listing using pricing and quality rules.
5. The user receives a Purchase Confidence Score, recommendation, and supporting insights.

---

# Features

✅ Upload Marketplace screenshots

✅ OCR text extraction (EasyOCR)

✅ Local AI listing analysis (Granite 3.2 Vision via Ollama)

✅ Purchase Confidence Score

✅ Rule-based recommendation engine

✅ Animated loading experience

✅ Screenshot preview during analysis

✅ Modern React interface

---

# Supported Products (Version 1)

### 📱 Phones

- iPhone
- Samsung Galaxy
- Google Pixel

### 💻 Laptops

- MacBook
- Microsoft Surface
- Dell
- HP
- Lenovo

### 🎮 Gaming

- PlayStation 4
- PlayStation 5
- Xbox
- Nintendo Switch
- Steam Deck

### 🎧 Audio

- AirPods

### ⌚ Wearables

- Apple Watch

---

# Technology Stack

## Frontend

- React
- Vite
- CSS

## Backend

- FastAPI
- Python

## AI

- Ollama
- Granite 3.2 Vision
- EasyOCR

---

# System Architecture

```
Marketplace Screenshot
          │
          ▼
      EasyOCR
          │
          ▼
Text Cleanup
          │
          ▼
Granite AI
(Listing Extraction)
          │
          ▼
Scout Engine
(Confidence Scoring)
          │
          ▼
React UI
```

---

# Repository Structure

```
ScoutAI/

├── backend/
│   ├── analyzer.py
│   ├── granite.py
│   ├── main.py
│   ├── ocr.py
│   ├── pricing.py
│   ├── prompts.py
│   └── scout_engine.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── README.md
└── .gitignore
```

---

# Running Locally

## Backend

```bash
cd backend

venv\Scripts\activate

uvicorn main:app --reload
```

Backend runs on:

```
http://127.0.0.1:8000
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on:

```
http://localhost:5173
```

---

# Current MVP Limitations

This project is an MVP designed to demonstrate the complete AI workflow.

Current limitations include:

- OCR may occasionally miss symbols or browser artifacts.
- Market value ranges are curated rather than live.
- Product support is currently focused on common consumer electronics.
- Seller history and account reputation are not yet evaluated.

---

# Future Roadmap

### Version 2

- Live marketplace pricing
- Better OCR cleanup
- Expanded product support
- Improved scoring

### Version 3

- Seller trust analysis
- Scam detection
- Historical pricing
- Browser extension

### Version 4

- Mobile application
- Personalized buying recommendations
- Marketplace integrations

---

# Team

Arizona State University

Scout AI

2026

---

# License

This project is intended for educational purposes.