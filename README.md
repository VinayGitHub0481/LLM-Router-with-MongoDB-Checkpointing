# 🤖 AI Multi-LLM Router (LangGraph + Gemini + GPT + MongoDB)

## 📌 Overview

This project is a **multi-LLM routing system** built using LangGraph. It intelligently routes user queries through different models based on response quality.

It uses:
- 🧠 Google Gemini → Primary response generator  
- ⚖️ GPT Score Evaluator → Rates response (0–10)  
- 🔁 GPT-4.1-mini → Fallback for weak responses  
- 💾 MongoDB → Persistent memory (checkpointing)

---

## 🚀 Workflow

User Query → Gemini → Score Evaluator → Decision:
- Score ≥ 8.5 → Accept Gemini response  
- Score < 8.5 → GPT fallback response  
→ Store final state in MongoDB  

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
