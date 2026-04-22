# agent.py

import os
import re
from dotenv import load_dotenv
from typing import TypedDict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from rag import get_relevant_info
from tools import mock_lead_capture

load_dotenv()

# ─────────────────────────────
# STATE
# ─────────────────────────────
class AgentState(TypedDict):
    messages: List
    intent: str
    lead_name: str
    lead_email: str
    lead_platform: str
    lead_captured: bool
    collecting_lead: bool


# ─────────────────────────────
# LLM (ONLY USED FOR RESPONSE)
# ─────────────────────────────
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)


# ─────────────────────────────
# INTENT (RULE BASED - NO API)
# ─────────────────────────────
def detect_intent(state: AgentState) -> AgentState:
    msg = state["messages"][-1].content.lower()

    if any(x in msg for x in ["buy", "try", "subscribe", "start"]):
        intent = "high_intent"
    elif any(x in msg for x in ["price", "plan", "cost", "feature"]):
        intent = "product_inquiry"
    elif any(x in msg for x in ["hi", "hello", "hey"]):
        intent = "greeting"
    else:
        intent = state.get("intent", "product_inquiry")  # maintain flow

    print(f"[DEBUG] Intent: {intent}")
    state["intent"] = intent
    return state


# ─────────────────────────────
# LEAD EXTRACTION (NO LLM)
# ─────────────────────────────
def extract_lead_info(state: AgentState) -> AgentState:
    msg = state["messages"][-1].content

    # Email
    if not state["lead_email"]:
        email = re.findall(r'\S+@\S+', msg)
        if email:
            state["lead_email"] = email[0]
            print("[DEBUG] Email:", state["lead_email"])

    # Name
    if not state["lead_name"]:
        if "name is" in msg.lower():
            state["lead_name"] = msg.split("is")[-1].strip()
        elif len(msg.split()) == 1:
            state["lead_name"] = msg.strip()

    # Platform
    if not state["lead_platform"]:
        for p in ["youtube", "instagram", "tiktok"]:
            if p in msg.lower():
                state["lead_platform"] = p.capitalize()
                print("[DEBUG] Platform:", state["lead_platform"])

    return state


# ─────────────────────────────
# RESPONSE
# ─────────────────────────────
def agent_respond(state: AgentState) -> AgentState:
    kb = get_relevant_info(state["messages"][-1].content)

    system_prompt = f"""
You are AutoStream AI assistant.

Answer using knowledge below:
{kb}

If collecting lead:
Ask only ONE missing field at a time.
"""

    # Lead collection manual flow (NO LLM confusion)
    if state["intent"] == "high_intent":
        state["collecting_lead"] = True

    if state["collecting_lead"]:
        if not state["lead_name"]:
            reply = "Great! What's your name?"
        elif not state["lead_email"]:
            reply = "Please provide your email."
        elif not state["lead_platform"]:
            reply = "Which platform do you create content on?"
        else:
            reply = "Processing your details..."
        
        state["messages"].append(AIMessage(content=reply))
        return state

    # Normal LLM response
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        *state["messages"]
    ])

    state["messages"].append(AIMessage(content=response.content))
    return state


# ─────────────────────────────
# CAPTURE LEAD (FIXED)
# ─────────────────────────────
def capture_lead(state: AgentState) -> AgentState:
    print("[DEBUG] Checking lead capture...")

    if (
        state["lead_name"] and
        state["lead_email"] and
        state["lead_platform"] and
        not state["lead_captured"]
    ):
        print("[DEBUG] Calling mock_lead_capture...")

        mock_lead_capture(
            state["lead_name"],
            state["lead_email"],
            state["lead_platform"]
        )

        state["lead_captured"] = True

        confirmation = f"""
✅ LEAD CAPTURED SUCCESSFULLY!

Name: {state['lead_name']}
Email: {state['lead_email']}
Platform: {state['lead_platform']}

We’ll contact you soon 🚀
"""
        state["messages"].append(AIMessage(content=confirmation))

    return state


# ─────────────────────────────
# ROUTER (FIXED)
# ─────────────────────────────
def router(state: AgentState) -> str:

    # Trigger capture IMMEDIATELY
    if (
        state["lead_name"] and
        state["lead_email"] and
        state["lead_platform"] and
        not state["lead_captured"]
    ):
        print("[DEBUG] → CAPTURE")
        return "capture"

    if state["intent"] == "high_intent" or state["collecting_lead"]:
        print("[DEBUG] → LEAD FLOW")
        return "extract_and_respond"

    print("[DEBUG] → NORMAL")
    return "respond"


# ─────────────────────────────
# GRAPH
# ─────────────────────────────
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("detect_intent", detect_intent)
    graph.add_node("respond", agent_respond)
    graph.add_node("extract_lead", extract_lead_info)
    graph.add_node("respond_lead", agent_respond)
    graph.add_node("capture", capture_lead)

    graph.set_entry_point("detect_intent")

    graph.add_conditional_edges(
        "detect_intent",
        router,
        {
            "respond": "respond",
            "extract_and_respond": "extract_lead",
            "capture": "capture"
        }
    )

    graph.add_edge("extract_lead", "respond_lead")
    graph.add_edge("respond_lead", END)
    graph.add_edge("respond", END)
    graph.add_edge("capture", END)

    return graph.compile()


# ─────────────────────────────
# MAIN
# ─────────────────────────────
def run_agent():
    print("\n🎬 AutoStream AI Agent\n")

    agent = build_graph()

    state: AgentState = {
        "messages": [],
        "intent": "",
        "lead_name": "",
        "lead_email": "",
        "lead_platform": "",
        "lead_captured": False,
        "collecting_lead": False
    }

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        state["messages"].append(HumanMessage(content=user_input))
        state = agent.invoke(state)

        ai_msgs = [m for m in state["messages"] if isinstance(m, AIMessage)]
        if ai_msgs:
            print("Agent:", ai_msgs[-1].content)


if __name__ == "__main__":
    run_agent()