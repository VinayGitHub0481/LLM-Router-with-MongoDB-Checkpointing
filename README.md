# 🤖 AI Multi-LLM Router with MongoDB Checkpointing (LangGraph)

## 📌 Overview

This project is a **multi-LLM routing system** built using LangGraph.

It routes user queries through different language models based on response quality using a scoring mechanism and maintains persistent state using MongoDB.

---

## ⚙️ Architecture

User Query
↓
Gemini Model (Primary Response)
↓
Score Evaluator (0–10)
↓
IF score ≥ 8.5 → Accept Gemini response
IF score < 8.5 → GPT-4.1-mini fallback
↓
MongoDB Checkpointer (State Persistence)

---

## 🧠 Core Idea

Instead of using one model:
- Gemini generates response first  
- GPT evaluates quality  
- GPT is used only when needed (fallback system)  
- MongoDB stores conversation state permanently  

---

## ⚙️ Tech Stack

- Python 🐍  
- LangGraph 🔗  
- LangChain 🤖 (Gemini + GPT-4.1-mini)  
- MongoDB 💾 (Checkpoint memory)  
- Pydantic 📦 (structured scoring)  
- Docker 🐳  
- dotenv 🔐  
---

## ▶️ Setup 

### 1. Install dependencies
```bash
pip install -r requirements.txt
