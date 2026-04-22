# AutoStream AI Sales Agent

## Overview

This project implements a conversational AI agent for **AutoStream**, a SaaS platform for automated video editing.

The agent is capable of:

* Detecting user intent
* Answering product queries using a knowledge base (RAG)
* Identifying high-intent users
* Collecting lead details step-by-step
* Executing a backend tool to capture leads

---

## Key Features

### 1. Intent Detection

The agent classifies user input into:

* greeting
* product_inquiry
* high_intent

This is implemented using a **rule-based approach** for reliability and reduced API usage.

---

### 2. RAG (Retrieval-Augmented Generation)

The agent retrieves product information from a local JSON knowledge base.

Includes:

* Pricing plans
* Features
* Policies

Ensures accurate and grounded responses.

---

### 3. Lead Qualification Flow

When a user shows high intent:

* The agent enters **lead collection mode**
* It asks for:

  * Name
  * Email
  * Platform
* It collects one field at a time

---

### 4. Tool Execution (Critical Feature)

Once all details are collected, the agent triggers:

```python
mock_lead_capture(name, email, platform)
```

This prints a confirmation in the terminal.

---

## Sample Output (Actual Run)

```text
You: I want to try the Pro plan for my Youtube channel
[DEBUG] Intent: high_intent
[DEBUG] → LEAD FLOW

Agent: Great! What's your name?

You: Thahaseena
Agent: Please provide your email.

You: thahaseenashaik0517@gmail.com
[DEBUG] Email: thahaseenashaik0517@gmail.com

Agent: Processing your details...

You: Youtube
[DEBUG] → CAPTURE
[DEBUG] Calling mock_lead_capture...

LEAD CAPTURED SUCCESSFULLY!
Name     : Thahaseena
Email    : thahaseenashaik0517@gmail.com
Platform : Youtube
```

---

## State Management

The agent maintains state using LangGraph.

Tracked values:

* conversation history
* intent
* lead_name
* lead_email
* lead_platform
* lead_captured flag

This ensures correct multi-turn conversation flow.

---

## Tech Stack

* Python 3.9+
* LangGraph
* LangChain
* Google Gemini (gemini-1.5-flash)
* JSON (knowledge base)

---

## Project Structure

```
autostream-agent/
│
├── agent.py
├── rag.py
├── tools.py
├── knowledge_base.json
├── requirements.txt
├── README.md
└── .env
```

---

## How to Run

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Add API key

Create `.env` file:

```
GOOGLE_API_KEY=your_api_key
```

### 3. Run

```
python agent.py
```

---

## Architecture Explanation

This project uses **LangGraph** to implement a structured agent workflow.

Flow:

1. User input enters the system
2. Intent is detected using rule-based logic
3. If product query → RAG is used
4. If high intent → lead collection starts
5. Data is extracted using deterministic logic (regex + rules)
6. Once all fields are available → tool execution is triggered

LangGraph manages transitions between:

* intent detection
* response generation
* lead extraction
* tool execution

State is maintained across all steps to ensure consistency.

---

## WhatsApp Integration (Concept)

To integrate with WhatsApp:

1. Use WhatsApp Business API (Meta or Twilio)
2. Create a backend (FastAPI/Flask)
3. Configure webhook to receive messages
4. Pass messages to agent
5. Send responses back via API
6. Store user state using phone number

Flow:

User → WhatsApp → Webhook → Backend → Agent → Response → WhatsApp

---

## Future Improvements

* Vector database for semantic RAG (FAISS)
* Database storage for leads
* Deployment with FastAPI
* Multi-user session handling

---

## Author

Shaik Mahaboob Thahaseena
