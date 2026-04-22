# AutoStream AI Sales Agent

## Overview

This project implements a conversational AI agent for **AutoStream**, a SaaS platform that provides automated video editing tools for content creators.

The agent is designed to:

* Understand user intent
* Answer product queries using a knowledge base (RAG)
* Identify high-intent users
* Collect lead details step-by-step
* Execute a backend tool to capture leads

---

## Key Features

### 1. Intent Detection

The agent classifies user input into:

* greeting
* product_inquiry
* high_intent

This is implemented using a **rule-based approach** for reliability and efficiency.

---

### 2. RAG (Retrieval-Augmented Generation)

The agent retrieves product information from a local JSON knowledge base.

Includes:

* Pricing plans
* Features
* Policies

This ensures accurate and grounded responses.

---

### 3. Lead Qualification Flow

When a user shows high intent:

* The agent enters **lead collection mode**
* It asks for:

  * Name
  * Email
  * Platform
* It collects one field at a time
* Maintains state across multiple turns

---

### 4. Tool Execution (Core Requirement)

Once all details are collected, the agent triggers:

```python
mock_lead_capture(name, email, platform)
```

This simulates a backend API call and confirms successful lead capture.

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

The agent uses LangGraph to maintain state across multiple conversation turns.

Tracked values:

* Conversation history
* Intent
* Lead name
* Lead email
* Lead platform
* Lead captured flag

This ensures correct multi-step flow and prevents premature tool execution.

---

## Tech Stack

* Python 3.9+
* LangGraph (stateful workflow)
* LangChain
* Google Gemini (**gemini-2.5-flash-lite**)
* JSON (knowledge base)

---

## Model Details

The system uses **Gemini 2.5 Flash-Lite**, which supports:

* ~15 requests per minute
* ~1000 requests per day

This makes it suitable for high-speed and efficient interactions.

To optimize usage:

* Intent detection is rule-based
* Lead extraction uses regex
* LLM is used only for response generation

---

## Project Structure

```
autostream-agent/
│
├── data/
│   └── knowledge_base.json
├── agent.py
├── rag.py
├── tools.py
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

Create a `.env` file:

```
GOOGLE_API_KEY=your_api_key_here
```

### 3. Run the agent

```
python agent.py
```

---

## Architecture Explanation

This project uses **LangGraph** to implement a structured agent workflow.

Flow:

1. User input is received
2. Intent is detected using rule-based logic
3. If product query → RAG retrieves knowledge
4. If high intent → lead collection starts
5. Lead details are extracted using deterministic logic (regex + rules)
6. Once all fields are available → tool execution is triggered

LangGraph manages transitions between:

* intent detection
* response generation
* lead extraction
* tool execution

State is preserved across all steps, enabling consistent multi-turn conversations.

---

## WhatsApp Integration (Concept)

To integrate this agent with WhatsApp:

1. Use WhatsApp Business API (Meta or Twilio)
2. Create a backend using FastAPI or Flask
3. Configure a webhook to receive user messages
4. Pass messages to the agent
5. Send responses back via WhatsApp API
6. Store user state using a database (e.g., Redis) with phone number as key

Flow:

```
User → WhatsApp → Webhook → Backend → Agent → Response → WhatsApp
```

---

## Future Improvements

* Use vector database (FAISS) for semantic RAG
* Store leads in a database instead of mock function
* Deploy using FastAPI
* Add multi-user session handling

---

## Author

Shaik Mahaboob Thahaseena
