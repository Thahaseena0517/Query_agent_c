# AutoStream AI Sales Agent

A conversational AI agent built for AutoStream, a SaaS video editing platform. This agent handles product inquiries, detects high-intent users, and captures leads automatically.

---

## How to Run Locally

### Prerequisites
- Python 3.9+
- A free Gemini API key from [Google AI Studio](https://aistudio.google.com)

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/autostream-agent.git
cd autostream-agent

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
# Create a .env file and add:
# GOOGLE_API_KEY=your_key_here

# 5. Run the agent
python agent.py
```

---

## Architecture Explanation (~200 words)

This agent is built using **LangGraph**, a framework for building stateful, multi-step AI agents as graphs. I chose LangGraph over AutoGen because it offers explicit control over the conversation flow through a directed graph of nodes — making it easier to enforce rules like "don't trigger lead capture until all three fields are collected."

The architecture consists of five nodes:

1. **detect_intent** — classifies every user message as `greeting`, `product_inquiry`, or `high_intent` using the LLM
2. **respond** — generates a context-aware reply using the knowledge base (RAG)
3. **extract_lead** — parses name, email, and platform from user messages using structured LLM extraction
4. **respond_lead** — continues the lead collection conversation
5. **capture** — calls `mock_lead_capture()` only when all three fields are filled

**State management** is handled via LangGraph's `StateGraph` with a typed `AgentState` dictionary that persists across all conversation turns. This holds the full message history, detected intent, collected lead fields, and flags for lead collection progress — ensuring the agent never loses context across 5–6 turns.

---

## WhatsApp Deployment via Webhooks

To deploy this agent on WhatsApp:

1. **Use Meta's WhatsApp Business API** (via Twilio or Meta directly)
2. **Set up a Webhook endpoint** using FastAPI or Flask:
   - When a user sends a WhatsApp message, Meta sends a POST request to your webhook URL
   - Your server receives the message, processes it through the LangGraph agent, and sends back a reply via the WhatsApp API
3. **Session management**: Store each user's `AgentState` in Redis or a database keyed by their WhatsApp phone number, so each user has their own persistent conversation thread
4. **Deploy** the FastAPI server on Railway, Render, or AWS

```
WhatsApp User → Meta Webhook → FastAPI Server → LangGraph Agent → Gemini LLM → Response → WhatsApp User
```