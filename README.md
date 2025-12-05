# ContextFlow  
## Extract insights from conversation history, then ask questions with customizable tone.
ContextFlow is designed as a modular, transparent conversational intelligence stack. 
The backend is built with Flask and organized into clear route, service, memory, and 
personality modules. Gemini Flash Lite generates structured outputs and rewritten responses. 
ChromaDB stores vectorized preferences and behavioral patterns, while SQLite holds factual 
entries. The frontend is a single-page, framework-free interface (HTML + CSS + JS) that 
visualizes every stage of the pipeline: memory extraction, storage, raw model response, 
and personality transformation.

---

![Architecture](screenshots/architecture.svg)

---
```
flowchart LR
  subgraph UI [Frontend]
    A[HTML / CSS / Vanilla JS]
  end

  subgraph API [Flask API]
    B[/memory/extract\n/personality/transform/]
  end

  subgraph LLM [Gemini]
    C[(Gemini Flash-Lite)]
  end

  subgraph Storage [Storage]
    D[ChromaDB (vectors)]
    E[SQLite (facts)]
  end

  A --> B
  B --> C
  B --> D
  B --> E
  C --> B
```

---
## 📸 Interface Preview

### **Initial Interface**
Before any extraction or generation:
![Initial UI](screenshots/screenshot_initial.png)

### **After Memory Extraction + Personality Response**
Full system behavior demonstrated:
![Final UI](screenshots/screenshot_final.png)

---
```bash
                         ┌─────────────────────────┐
                         │       Frontend UI       │
                         │  HTML • CSS • Vanilla JS│
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │        Flask API        │
                         │  /memory   /personality │
                         └─────┬──────────┬────────┘
                               │          │
                 ┌─────────────┘          └──────────────┐
                 ▼                                       ▼
      ┌──────────────────────┐                ┌────────────────────────┐
      │  Memory Extraction   │                │   Personality Engine   │
      │    extractor.py      │                │       engine.py        │
      └─────────┬────────────┘                └──────────┬─────────────┘
                │                                        │
                ▼                                        ▼
     ┌──────────────────────┐                 ┌───────────────────────┐
     │   Gemini Flash Lite  │ <──────────────►│  Gemini Rewrite Call  │
     └─────────┬────────────┘                 └────────┬──────────────┘
               │                                       │
      ┌────────┴────────┐                     ┌────────┴──────────┐
      ▼                 ▼                     ▼                   ▼
┌────────────────┐ ┌───────────────┐   ┌────────────────┐ ┌─────────────────────┐
│    ChromaDB    │ │   SQLite DB   │   │  Raw Response  │ │ Personality Output  │
│ vector storage │ │    facts.db   │   │    (before)    │ │       (after)       │
└────────────────┘ └───────────────┘   └────────────────┘ └─────────────────────┘
```
## 🧠 Overview

ContextFlow showcases three core capabilities:

### **1. Memory Extraction Engine**
Users can input up to 30 chat messages.  
The system extracts:

- **User Preferences**  
- **Emotional Patterns**  
- **Factual Information**

These are stored in:
- **ChromaDB** → preferences and emotional patterns  
- **SQLite** → structured factual entries  

Extraction logic uses a strict JSON-only Gemini prompt to ensure machine-readable outputs.

### **2. Personality Transformation Engine**
ContextFlow transforms any raw Gemini answer into one of five professional styles:

- Calm Mentor  
- Witty Friend  
- Therapist-Style  
- Strict Analyst  
- Professional Corporate Tone  

All transformed outputs are limited to **six lines** to maintain conciseness and clarity.

### **3. Transparent UI**
All processes happen on a single page:
- Memory extraction  
- Storage results  
- Raw LLM answer  
- Tone-transformed answer  

Nothing is hidden. Every step is visible to the user.

---

## 📄 Example Conversation (DEMO)

A full 30-message fictional conversation demonstrating the extraction pipeline is included in:

### DEMO.md


This file shows exactly how the memory engine responds to real conversational structure.

---

## 🗂 Project Structure
```
ContextFlow/
│
├── backend/
│   ├── app.py                     # Main Flask entrypoint
│   ├── routes/
│   │   ├── memory_routes.py       # extracts memories + saves to ChromaDB & SQLite
│   │   ├── personality_routes.py  # Gemini raw answer + personality transformation
│   │   └── healthcheck.py         # Simple alive-check endpoint for Render
│   ├── memory/
│   │   ├── extractor.py           # Logic for prompting Gemini to extract structured memory
│   │   └── storage.py             # Interfaces for ChromaDB vector storage and SQLite facts
│   ├── personality/
│   │   └── engine.py              # Tone rewriting engine; applies selected personality rules
│   ├── services/
│   │   ├── gemini_client.py       # Low-level Gemini API caller; handles JSON + errors
│   │   └── utils.py               # Shared helpers: validation, formatting, small utilities
│   └── database/
│       └── facts.db          
│
├── templates/
│   └── index.html                 
│
├── DEMO.md                        
│
├── requirements.txt                            
└── README.md                 

```

---


---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/AlenKJ01/ContextFlow.git
cd ContextFlow
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate         # Windows
source venv/bin/activate      # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a .env file:
```
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=models/gemini-flash-lite-latest
```

### 5. Run the application
```bash
python backend/app.py
```

---

Access at:

### http://127.0.0.1:5000

---

## 🌐 Deployment (Render)

1. Push your project to GitHub.

2. Create a new Web Service on Render.

3. Configure:
```
Build Command: pip install -r requirements.txt
Start Command: python backend/app.py
```

4. Add environment variables:

- GEMINI_API_KEY
- GEMINI_MODEL=models/gemini-flash-lite-latest

5. Deploy.

---

## 💡 API Endpoints

### POST /memory/extract

Extract structured memory from conversation.

Input:
```
{
  "messages": ["Hi", "I prefer short answers", ...]
}
```

Output:
```
{
  "preferences": [...],
  "emotional_patterns": [...],
  "facts": [...]
}
```

### POST /personality/transform

Rewrite an answer into a specified tone.

Input:
```
{
  "text": "Explain gradient descent",
  "tone": "Strict Analyst"
}
```

Output:
```
{
  "before": "raw model answer",
  "after": "rewritten answer"
}
```
## 🧰 Tech Stack

Flask

ChromaDB

SQLite

Gemini Flash Lite

HTML, CSS, Vanilla JS

Python 3.10+

