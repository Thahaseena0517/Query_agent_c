# AutoStream AI Sales Agent

## Overview

This project implements a conversational AI agent for **AutoStream**, a SaaS (Software as a Service) platform that provides automated video editing tools for content creators.

The agent is designed to:

* Understand user intent
* Answer product queries using a knowledge base (RAG)
* Identify high-intent users
* Collect lead details step-by-step
* Execute a backend tool to capture leads

---

## Demo Video

Watch the demo here:
https://drive.google.com/file/d/1q_HkwXa_Ruauwrub30JHUGlYLcL8jMj6/view?usp=sharing

This demo showcases:

* RAG-based pricing response
* High-intent detection
* Lead qualification workflow
* Tool execution (`mock_lead_capture`)

---

## Core Features

### 1. Intent Detection

The agent classifies user input into:

* greeting
* product_inquiry
* high_intent

A **rule-based approach** is used for reliability and reduced API usage.

---

### 2. RAG Pipeline

The agent retrieves product information from a local JSON knowledge base.

Includes:

* Pricing plans
* Features
* Policies

This ensures accurate and grounded responses.

---

### 3. Lead Qualification Flow

When a user shows high intent:

* The agent enters lead collection mode
* It asks for:

  * Name
  * Email
  * Platform
* It collects one field at a time
* Maintains state across multiple turns

---

### 4. Tool Execution

Once all required details are collected, the agent triggers:

```python id="j3r2sn"
mock_lead_capture(name, email, platform)
```

This simulates a backend API call and confirms successful lead capture.

---

## Sample Output

```text id="0m8vgr"
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

## Tech Stack

* Python 3.9+
* LangGraph
* LangChain
* Google Gemini (**gemini-2.5-flash-lite**)
* JSON (knowledge base)

---

## Model Details

The system uses **Gemini 2.5 Flash-Lite**, which supports:

* ~15 requests per minute
* ~1000 requests per day

To optimize performance:

* Intent detection is rule-based
* Lead extraction uses regex
* LLM is used only for response generation

---

## Project Structure

```id="k1a8yc"
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

## How to Run Locally

### 1. Clone repository

```id="0w8mgh"
git clone https://github.com/YOUR_USERNAME/autostream-agent.git
cd autostream-agent
```

### 2. Create virtual environment

```id="1o6u0y"
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```id="e5khp0"
pip install -r requirements.txt
```

### 4. Add API key

Create a `.env` file:

```id="7a1x2v"
GOOGLE_API_KEY=your_api_key_here
```

### 5. Run the agent

```id="b9z9hg"
python agent.py
```

---

## Architecture Explanation

This project uses **LangGraph** to implement a structured, stateful conversational agent. LangGraph was chosen because it provides explicit control over agent behavior through nodes and transitions, making it ideal for enforcing conditions such as triggering tool execution only after all required user details are collected.

The system operates as a workflow of nodes:

* **Intent Detection Node**: Classifies user input using rule-based logic
* **RAG Module**: Retrieves relevant information from a local JSON knowledge base
* **Response Node**: Uses Gemini to generate contextual responses
* **Lead Extraction Node**: Extracts user details using deterministic logic (regex)
* **Tool Execution Node**: Calls `mock_lead_capture()` only when all required fields are available

State is managed using a structured dictionary (`AgentState`) that persists across conversation turns. It stores message history, intent, collected lead data, and flags such as `lead_captured`. This ensures consistent multi-turn interactions and prevents premature tool execution.

---

## WhatsApp Integration (Using Webhooks)

To integrate this agent with WhatsApp:

1. Use WhatsApp Business API (Meta or Twilio)
2. Build a backend server using FastAPI or Flask
3. Configure a webhook endpoint to receive incoming messages
4. When a message arrives:

   * Pass it to the agent
   * Process it using LangGraph
   * Generate a response
5. Send the response back via WhatsApp API
6. Store user state in a database (e.g., Redis) using phone number as key

### Flow

```id="f98y4q"
User → WhatsApp → Webhook → Backend → Agent → Response → WhatsApp
```

---

## Future Improvements

* Use vector database (FAISS) for semantic RAG
* Store leads in a real database
* Deploy using FastAPI
* Add multi-user session handling

---

## Author

Shaik Mahaboob Thahaseena
