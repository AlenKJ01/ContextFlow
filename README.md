# ContextFlow  
A modular conversational intelligence framework that demonstrates transparent memory extraction, controlled personality rewriting, and end-to-end reasoning flow using Gemini, Flask, ChromaDB, and SQLite.

ContextFlow provides a clear, auditable pipeline for how conversational agents can extract information from dialogue, store it as reusable memory, and apply personality-specific rewriting to new responses. The entire process is visible to the user, with no hidden state and no background processing.

---

## 📸 Interface Preview

### **Initial Interface**
Before any extraction or generation:
![Initial UI](screenshots/screenshot_initial.png)

### **After Memory Extraction + Personality Response**
Full system behavior demonstrated:
![Final UI](screenshots/screenshot_final.png)

---

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

